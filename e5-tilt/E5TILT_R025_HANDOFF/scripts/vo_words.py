"""G2: word timestamps for the locked VO -> audio/VO_WORDS.json (run locally; the cloud session cannot download models).
pip install faster-whisper ;  python scripts/vo_words.py [--model large-v3] [--audio audio/R024_ORIGINAL_AUDIO.m4a]
Then fill 'noun_first_F' in BEATS_R025.csv and rerun src/sync_qc.py.
"""
import json, os, argparse, hashlib
from faster_whisper import WhisperModel
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser()
ap.add_argument('--audio', default=os.path.join(ROOT, 'audio', 'R024_ORIGINAL_AUDIO.m4a'))
ap.add_argument('--model', default='large-v3')
ap.add_argument('--lang', default='ko')
a = ap.parse_args()
lock = json.load(open(os.path.join(ROOT, 'audio', 'VO_LOCK.json')))
sha = hashlib.sha256(open(a.audio, 'rb').read()).hexdigest()
assert sha == lock['sha256'], 'audio does not match VO_LOCK.json - re-record means a new LOCK'
m = WhisperModel(a.model, device='auto', compute_type='auto')
segs, info = m.transcribe(a.audio, language=a.lang, word_timestamps=True, vad_filter=False)
words, text = [], []
for s in segs:
    text.append(s.text.strip())
    for w in s.words:
        words.append({'w': w.word.strip(), 't0': round(w.start, 3), 't1': round(w.end, 3),
                      'F0': int(round(w.start * 30)) + 1, 'F1': int(round(w.end * 30)) + 1, 'p': round(w.probability, 3)})
json.dump({'audio_sha256': sha, 'model': a.model, 'text': text, 'words': words},
          open(os.path.join(ROOT, 'audio', 'VO_WORDS.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('\n'.join(text)); print(len(words), 'words')
