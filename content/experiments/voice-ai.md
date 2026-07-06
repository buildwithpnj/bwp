---
id: "EXP-02"
title: "Low-Latency Spoken Language Interfaces"
tagline: "Measuring response delay during WebRTC audio streaming to local language models."
status: "wip"
category: "Voice AI"
tags: ["voice", "webrtc", "llm"]
hypothesis: "Direct streaming of audio chunks over WebRTC to local transcription models keeps total latency under 200ms."
publishDate: "2026-07-02"
---

## Objective
To build a voice interface that lets users chat with local LLMs in real time with minimal latency.

## Methodology
- Stream microphone audio using WebRTC.
- Transcribe audio chunks in real time using a streaming Whisper model.
- Stream transcription tokens to a local LLM.
- Synthesize the model's text response to speech in real time.

## Findings
- Network latency was kept under 40ms using WebRTC.
- Whisper transcription speed is critical to keeping total latency under the 200ms target.
