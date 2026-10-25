"""Run: python -m unittest discover -s tests -v (FFmpeg/FFprobe must be available)."""
import json
import subprocess
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
APPLY = ROOT / 'scripts' / 'apply.py'


def run(cmd, check=True):
    return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, check=check)


class CapCutDualLookTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix='capcut-dual-skill-')
        cls.d = Path(cls.temp.name)
        cls.source = cls.d / 'sample_clip.mp4'
        run(['ffmpeg','-hide_banner','-loglevel','error','-y',
            '-f','lavfi','-i','testsrc2=size=320x568:rate=12:duration=0.6',
            '-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=0.6',
            '-map','0:v:0','-map','1:a:0','-t','0.6',
            '-c:v','libx264','-pix_fmt','yuv420p','-c:a','aac',
            '-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709',str(cls.source)])

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_lut_files(self):
        for name, n in [('CapCut_4K_Approx_33.cube',33), ('CapCut_Auto_Approx_49.cube',49),
                        ('BSK_4K_then_Auto_65.cube',65)]:
            file = ROOT / 'assets' / 'luts' / name
            self.assertTrue(file.is_file(), name)
            with file.open(encoding='utf-8') as stream:
                self.assertIn(f'LUT_3D_SIZE {n}', ''.join(stream.readline() for _ in range(4)))

    def test_dry_run(self):
        result=run([sys.executable,str(APPLY),str(self.source),'--dry-run'])
        self.assertIn('BSK_4K_then_Auto_65.cube',result.stdout)
        self.assertFalse((self.d/'sample_clip_BSK_4K_AUTO.mp4').exists())

    def test_transcode_and_chain_comparison(self):
        for eng in ('fused','chain'):
            d=self.d / eng
            run([sys.executable,str(APPLY),str(self.source),'--encoder','cpu', '--engine',eng,
                 '--output-dir',str(d)])
            target=d/'sample_clip_BSK_4K_AUTO.mp4'
            self.assertTrue(target.exists())
            report=json.loads((d/'sample_clip_BSK_4K_AUTO.grade.json').read_text(encoding='utf-8'))
            self.assertEqual(report['source_video']['width'],report['output_video']['width'])
            self.assertEqual(report['source_video']['height'],report['output_video']['height'])
            self.assertEqual(report['encoder'],'cpu')
            self.assertEqual(report['order'],'4k-auto')
            p=run(['ffprobe','-v','error','-select_streams','a','-show_entries','stream=codec_type',
                  '-of','default=noprint_wrappers=1',str(target)])
            self.assertIn('audio',p.stdout)
        # Capturing raw bytes with text=True (run helper) is unsuitable, use subprocess directly.
        args=lambda engine: ['ffmpeg','-v','error','-i',str(self.d/engine/'sample_clip_BSK_4K_AUTO.mp4'),
                             '-vf','scale=160:284','-f','rawvideo','-pix_fmt','rgb24','-']
        a=subprocess.run(args('fused'),capture_output=True,check=True).stdout
        b=subprocess.run(args('chain'),capture_output=True,check=True).stdout
        self.assertEqual(len(a),len(b))
        mae=sum(abs(x-y) for x,y in zip(a,b))/len(a)
        print(f'\n Fused-vs-chain actual FFmpeg encoded video RGB MAE: {mae:.3f}/255')
        self.assertLess(mae,5.0)

    def test_reverse_and_auto_only(self):
        for opts,suffix in [(['--order','auto-4k'],'_BSK_AUTO_4K.mp4'),
                            (['--mode','auto'],'_BSK_AUTO.mp4')]:
            d=self.d/('reverse' if 'auto-4k' in opts else 'auto')
            run([sys.executable,str(APPLY),str(self.source),'--encoder','cpu',
                 '--output-dir',str(d),*opts])
            self.assertTrue((d/('sample_clip'+suffix)).is_file())

    def test_hdr_rejected(self):
        fake=self.d/'fake_hdr.mp4'
        run(['ffmpeg','-hide_banner','-loglevel','error','-y',
             '-f','lavfi','-i','testsrc2=size=320x568:rate=12:duration=0.6',
             '-c:v','libx264','-pix_fmt','yuv420p',
             '-color_primaries','bt2020','-color_trc','smpte2084','-colorspace','bt2020nc',str(fake)])
        outcome=run([sys.executable,str(APPLY),str(fake),'--encoder','cpu'],check=False)
        self.assertNotEqual(outcome.returncode,0)
        self.assertFalse((self.d/'fake_hdr_BSK_4K_AUTO.mp4').exists())

    def test_compare_grid(self):
        d=self.d/'compare'
        run([sys.executable,str(ROOT/'scripts'/'compare.py'),str(self.source),'--at','0.2','--video','0.4',
             '--scale','0.5','--output-dir',str(d)])
        img=d/'sample_clip_BSK_COMPARE_0.2s.jpg'
        vid=d/'sample_clip_BSK_COMPARE_0.4s.mp4'
        self.assertTrue(img.is_file()); self.assertTrue(vid.is_file())
        for f in (img,vid):
            p=run(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height',
                   '-of','csv=p=0',str(f)])
            w,h=[int(x) for x in p.stdout.strip().split(',')[:2]]
            # 320x568 소스 → 패널 160x284 → 2x2 그리드 320x568
            self.assertEqual((w,h),(320,568),f.name)
        # 비교 결과물은 일괄 처리 대상에서 제외되어야 한다
        dry=run([sys.executable,str(APPLY),str(d),'--dry-run'],check=False)
        self.assertIn('처리할 비디오 파일이 없습니다',dry.stdout+dry.stderr)


if __name__=='__main__':
    unittest.main()
