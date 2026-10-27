# audio/

음성 락(G2)은 ChatGPT 최종 대본 → ElevenLabs(RMC와 같은 보이스) 녹음 후 진행한다.
- `VO_LOCK.json` : 파일명, sha256, 길이(초), 샘플레이트
- `VO_WORDS.json` : 단어 타임스탬프(faster-whisper word_timestamps=True)
- `SFX_CUES.csv` : F, 종류, 레이어, 원본 파일, 라이선스 (사건 F는 src/rig_config.json.events)
대본은 SCENARIO_v1.md §2 의 음절 예산과 명사 위치를 지켜야 한다.
