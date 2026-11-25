# 🤖 [2026.11.18 ~ 2026.11.25] 주간 IT · AI 핵심 이슈 리포트 (4대 심층분석 + 단신 8선)

> **자동 수집 시각**: `2026-11-25 18:36:12 KST` (매주 수요일 10:00 KST)  |  **수신**: `@starjw2010-cloud`
>
> - 📊 **[8장 영상용 마스터 슬라이드 열기 (Google Slides)](https://docs.google.com/presentation/d/1yad5aoY8SAX-fImKETc520AsWWwWwPvWojVLGJTKQ68/edit)**
> - 📁 **[AI Tech News 드라이브 폴더](https://drive.google.com/drive/folders/107pVU_TPQS6USbFJsPsf4o_aRBB5TTKc)**
> - 🗂️ **[02_Weekly_Briefings (주간 슬라이드·PDF)](https://drive.google.com/drive/folders/1wiIpcQGPbBwOqu9t_JxJg2C9LOhQSa60)**
> - 🎬 **[03_Weekly_Videos (아바타·자막 MP4)](https://drive.google.com/drive/folders/18gcOJM175VVxb7rgq0wcuU-1u2bISSdI)**

---

## 📌 파트 0. 사용자 지정 필수 반영 이슈 (Pinned Topics)

### [AI 모델 · 에이전트 · 오픈 웨이트] Thinking Machines Lab, 오픈 웨이트 'Inkling 2 Mini' 및 학습 API 'Tinker · Tinker Cookbook' 생태계 공개 (`2026-11-20`)
- **요약**: 전 OpenAI CTO 미라 무라티 등이 설립한 Thinking Machines Lab이 오픈 웨이트 학습 API 'Tinker'(LoRA 공유 연산 풀 기반 SFT/RL 루프 제어) 및 오픈소스 레시피 'Tinker Cookbook'과 함께 로컬 구동 특화 멀티모달 모델 'Inkling 2 Mini'(Apache 2.0)를 Hugging Face와 Tinker에 동시 공개.
  - Looped Transformer + MoE: 총 26.4B(활성 3.4B) 24개 레이어 중 중간 12개 레이어를 가중치 공유로 3회 반복 → 48개 유효 레이어(유효 활성 5.4B) 추론·코딩 성능 확보
  - 네이티브 저비트 학습: 앞단 20개 레이어 NVFP4 + 마지막 4개 레이어 MXFP8 네이티브 학습(PTQ 성능 저하 없음), 단일 체크포인트 약 20GB
  - 로컬 구동 및 에이전트 성능: 텍스트·이미지 멀티모달 + 1M 컨텍스트, 32GB+ Apple Silicon Mac(Ollama/Unsloth/llama.cpp) 및 NVIDIA DGX Spark 구동 가능
  - 벤치마크: DeepSWE v1.1 48.2%, SWEBench Pro v2(Hard) 77.9%, 스탠퍼드 DGX Spark 에너지당 지능 0.703(Qwen3.6-35B-A3B 0.430 대비 우위)
  - 실무 배포 포인트: Tinker는 LoRA 기반 연구·후학습 특화 API이며 상시 추론 호스팅 대체재가 아니므로, 학습 완료 체크포인트를 추출해 vLLM·SGLang·Ollama 등 별도 서빙 인프라로 이관하는 파이프라인 설계 필요
- **공식 출처**: [Thinking Machines Lab 공식 발표](https://thinkingmachines.ai/news/inkling-2-mini/) · [Hugging Face 모델 카드 (Apache 2.0)](https://huggingface.co/thinkingmachines/Inkling-2-Mini) · [Tinker 학습 API](https://thinkingmachines.ai/tinker/) · [VentureBeat 심층 분석](https://venturebeat.com/technology/thinking-machines-wows-with-inkling-2-mini-looped-transformer-model-that-runs-locally-on-laptops)

---

## 🧠 파트 1. 주간 IT · AI 4대 핵심 영역 심층 스캔 (직전 7일)

### 01. [AI 모델 · 에이전트 · 오픈 웨이트] (실리콘밸리 · 글로벌 AI 랩 · 오픈소스 · 3p 심층분석)
- **핵심 헤드라인**: **[허깅페이스, 코딩 에이전트 맞춤 어댑터 공개…'큐원' 고난도 평가 39%→65%](https://news.google.com/rss/articles/CBMiakFVX3lxTE1pNHVocnBiWkpTRWdVYzgyWl8zeTV5d1gyWHZtdHRxbVBXWlUySHpaUEpwTTZ3OHMxRnEyckxyZkxKUnpVV0NZYUROQ0tIZ2tNOFpjLTl5eDNxZDNxX0JzY0JaOFZRN2lZUkE?oc=5)** (`AI타임스`, 11/19 17:23)
- **연관 교차검증 기사 (글로벌·국내)**:
  - 🇰🇷 [“경고에도 AI 테스트 계속”···캘리포니아주, 오픈AI 안전 관리에 책임 묻는다](https://news.google.com/rss/articles/CBMi3gJBVV95cUxPdmt6bWFyRDJnRWVlcFg2R0xBNDdTdUN6aTNEZ09aMGFvZXd6VkVTejdjamIzX1Z2S1cwR0pPc1BRaHZLeFR6bE1nTGdzdGZXdXg5Yjd3b1RGaHN2TFBiTjdiYnc4eFY4TmJJUlhRc1pIR2g0bzBaWlVmY3RFMV8tazI1M2JWMmNVcUZ3cm40MHdPdmV3a3VOa2paSkNyZi1CLWMtVm1lLUotTDdZbUtJSVdZclNwS08zbFV5LXRTVWxvbHpBempNUlhLOEtPdVhtLUpTbThIeThpZklMRHR0SnBfR1dldGJCc2xyMjNGQm8ySlZaUGxEdktUWmdSVDhISmtya2J4SU5VNHlIT1d3MnRzaWI5ZHFLQWNrNkJZaHhzTW9MYTc1RDFVRUhQcHR5YzV0WTJqLWNCQVJQcEZWbGlfcjdCUzBKT2VSQUs2UUcwdUVXNWR0clFSMGlvUQ?oc=5) (`www.cio.com`, 11/20 17:28)
  - 🇰🇷 [AMD, 언슬로스 데스크톱용 세계 최초 NPU 구현…100개 이상 AI 에이전트 온디바이스 실행 지원](https://news.google.com/rss/articles/CBMiZ0FVX3lxTFBUc3BaMWtYbE9VWHBQdnBvbExtR042UmRWTWNTYVZRbTFfSGNjb0JDSndmd0p1bXhoVUU5dFlwTlltOUtBdGVlcnVDNmR0aTJhdlM0NXI0WTN0RzhYTW0xT3d4ZDVnMlk?oc=5) (`인공지능신문`, 11/20 10:39)
  - 🌐 [Perplexity and Intelligence](https://news.google.com/rss/articles/CBMiY0FVX3lxTE96Sm1EaVlsMHctNGtBMDBYdVRreWpySVdVS1RhSVZCUzk3enZHQmlIS3lWY2Rmajh2Q3RNZWU2RDEwc3ZEX2tONEpsbEN6RXowZk1ySVdaWXVVR09jX21aelV6UQ?oc=5) (`OpenAI`, 11/23 04:12)
  - 🌐 [Working with AI](https://news.google.com/rss/articles/CBMiX0FVX3lxTE5QQWdUV21Fa2dHR25yU2RLd3Exd0ZQc3RERzMyZFBtWWhxS0NQZjlWR21rWXZqa3FYbmRlZEhPRGhXb19XR3UtTWd3YTdDR3JwM05VTzZoaW82UDdGQWNF?oc=5) (`Anthropic`, 11/24 06:12)

### 02. [AI 반도체 · 인프라] (미국 · 대만 · 한국 · 4p 심층분석)
- **핵심 헤드라인**: **[전력반도체 시장 규모, 2031년 92조원…AI·로봇이 성장 이끌어](https://news.google.com/rss/articles/CBMiTkFVX3lxTE54bmlGV3RBdlo0eVZ1cmROT2V0ejhRRm5IN0VERlpkcXNKTmYyeXZzNU1pODdKWU14MzN2R1djQmtEUlhRYlR2ZjQzQURUdw?oc=5)** (`전자신문`, 11/23 14:05)
- **연관 교차검증 기사 (글로벌·국내)**:
  - 🇰🇷 [KCL-부천시, AI 전력반도체 산업 육성 위한 전략적 협력 본격화](https://news.google.com/rss/articles/CBMibEFVX3lxTFBZR09QMHc4V212eVBPV25uN3BWbG80d3kzOWtrbWh5Tms4aV81Tk55NGpjU2puOGhFcmFwX2dDSEpqdjMzSVhsVTFSZGU2TE5qYkVYYkc5cGU3U2VPY2NLaVB5NlRIbUw1eFBCVNIBcEFVX3lxTFByalE5djhLUWxtd3ZkVkNoQ3o2Y3hnSXNUb2Y3bG01ejRXWVZHWHNfaWZHdjNsOE9NY1ZHN0lNWl9KenIzbS1wbXc2SmxmWnFFTEYzeFdqOG5LenAyZmtRTHViX0dqVTdlWFdPZ3pwNFE?oc=5) (`전기신문`, 11/24 08:50)
  - 🇰🇷 [“AI 반도체 전력·집적 한계 넘는다”... 전북대, 저온 공정 기반 초저전력 인공시냅스 소자 개발](https://news.google.com/rss/articles/CBMiSEFVX3lxTE52VVNDSTdHeTRyenppOGhQU3BJM1d4dW9tMmllcEdJNEdTNENpQkFVOGZpZUsxUnNrb0lYLWV6OU5PRlNMZFBUbg?oc=5) (`특허뉴스`, 11/24 16:25)
  - 🌐 [Trump sealed deal for Nvidia to rehire Jensen Huang as CEO](https://news.google.com/rss/articles/CBMib0FVX3lxTE9ab2habU9pTTllNmRCRDdqTjgwQ3hsVFZDX1hhVkJxaVVCWHNhYjRHLXFMaWtnME41NGZ1Z1REMkh1d2Y0NUJGamJSdVJQcV9rZEV1aW9nUlhHQWN1WkFSU3RRMnZrNEpobEp5bVBoY9IBdEFVX3lxTFBXNkNGSW1MaGlybGVOX0YtaVI0YVFfd3NYMi1BenZKN2Ewd1JJT3NMMjdpaElsRF9jSThyVzBHYlg4dUxocjBjYnV1dml4czdrWHR4akNId1g3SVJYa0oyRkdEUHJPMnRUVFpkbUpxWHRtWUxE?oc=5) (`CNBC`, 11/24 00:08)
  - 🌐 [The Frantic White House Push to Get Jensen Huang Back](https://news.google.com/rss/articles/CBMieEFVX3lxTE1pRUxrRllGQzRjbm1mbkxwWi1pcGVDREtMYVFlTWt0c2RaMm4zSFZ0UTFIOHc3eVpiaS1xODducUx5T013ekU4czVXaUVmR2JUblZPNS03Qy1yNW9wNloyaGdWeHVBQUI1VVR5NTdfRUxfNTdvdG1pSA?oc=5) (`WSJ`, 11/24 11:00)

### 03. [빅테크 · 클라우드 · SaaS] (북미 빅테크 · 엔터프라이즈 · 5p 심층분석)
- **핵심 헤드라인**: **[AI 투자 안해서 웃었다? 애플, 엔비디아 ‘시총 왕좌’ 뺏었다](https://news.google.com/rss/articles/CBMiVkFVX3lxTE1QeDA5UG9XZWJSbEJTWmR0NTdXMncxY0pUc2k3WFplSm0wSzdXdU8tRWJWdVJjb2ZudlNWU080aHhDbG9EdjN3Z01ac2hiY1hzTktVVGRB?oc=5)** (`중앙일보`, 11/25 18:01)
- **연관 교차검증 기사 (글로벌·국내)**:
  - 🇰🇷 [[2027 월가의 선택②] AI 투자 1조달러 시대…빅테크 수익화·기업 생산성 혁신에 주목](https://news.google.com/rss/articles/CBMibEFVX3lxTE5OM0ZVdTdadlZUSlNTMy1Gc2F0Z18wa3NIellVZ1h3blh3dUVhVGQ1UDZPbzlHNVd4bW9JRWx0Tm5sYk5ISkZ6TEtLTmFRSXlVem03T0phY1F5RV9xM2VjRHp5ZzdEbkMwY294Nw?oc=5) (`뉴시안`, 11/21 07:05)
  - 🇰🇷 [[美 AI 투자 시험대] ② 번 돈보다 더 쓴 美 빅테크…'돈줄' 마르는 기업들](https://news.google.com/rss/articles/CBMiXEFVX3lxTFBSZXZaNGM2QTNFekZWci0xcEJVSTlDaGVzQVpUY29EbEFOdlJick1RdGZRZThwbExqOERJbEFmMFNPc0MtQlcxRmNPbnY2Y0tEZ3doYTBaM25jZGFw?oc=5) (`뉴스핌`, 11/21 11:30)
  - 🌐 [Microsoft and Intel deepen collaboration to deliver differentiated Azure infrastructure](https://news.google.com/rss/articles/CBMizgFBVV95cUxNYTdtZG1GNmtwa1loVnhGcF9ZR2czUTVRRnZadmNXMFdrZDB6WWIzbWlUUmtVaHNpZDdjSHlqNkNfbThNY1dDYXM0M1lUb25hTldZMHpfdGNIZ29yVjE5R1RWUTE0MVR6MExyT21UQ3dUSk04eDdIMTVILVBXSWwzQVRZbnpfakstQVAzVFhMVlRBQmQ3T1dwdGJkNEczWGlCQUtNN2N2MEpaVGJySXFlZ2doTUV2bXdmZWxVUkNfcnl4SjlIenktakY5RFlSZw?oc=5) (`Microsoft Source`, 11/19 01:36)
  - 🌐 [Google Cloud Blows by Microsoft and AWS in New AI and Cloud Revenue](https://news.google.com/rss/articles/CBMimAFBVV95cUxNMEQzdk5HdmlXVmtKSG9BTExOaHY0QXp2d0IxQnFzLWEzbFR1MDE4YlBHUzhtbmtldVZTc19QUnBQdWc4LXYxNTJscGVQcWhxaGlSNTNQNTY5eFRzVFpaaVlOZ21BQWh1UU1pZHZNczRiWHdCR29zLXNqZkk5Qm5yenZzRVhlajB4UTRkZEhjeU52c3lKZHlKMg?oc=5) (`Cloud Wars`, 11/25 01:00)

### 04. [피지컬 AI · 보안 · 테크 정책] (미국 · 유럽 · 글로벌 규제 · 6p 심층분석)
- **핵심 헤드라인**: **[AI·로봇이 바꾸는 건설현장…25일부터 스마트건설 엑스포](https://news.google.com/rss/articles/CBMiW0FVX3lxTFBkUGR4Y0NxOEZYS1NpdHdITl9fT21IdmZhekw5MFRQX0NGeF81OUhkdUFoNVp0dlVYWEdwSDVEeC1sWHVwYmZlQmNnSXhBNzlRd2NxQ0dIM3daMGPSAWBBVV95cUxQcDd0bndoUVhZZE1aS3pkTVQwc1dMa2xnX1NiY0JqVlpURXVydE9wOGdyYjNPckdKcmdYMkgxbUE5V1hPLU1vbE03aXdVRXYxLUR5Nk9aaGFaUG0zMDJTS1k?oc=5)** (`연합뉴스`, 11/24 06:00)
- **연관 교차검증 기사 (글로벌·국내)**:
  - 🇰🇷 [LH, ‘2026 스마트건설·안전·AI EXPO’서 AI·로봇 기술 선보인다](https://news.google.com/rss/articles/CBMicEFVX3lxTE44MkU0eXBCYm9INkRlSjhXdzNCdFFMYWxfaERaMnZ0MFlNUTBsVVBmcHRxZHVzV3BkR2prd2NTeHZ3ZS1KSkJfY2RJZFlVaFpwbklwcVlTQnd1STFvUDNDTlJFaS1wVkl3VGhkSnhjdGjSAXBBVV95cUxOODJFNHlwQmJvSDZEZUo4V3czQnRRTGFsX2hEWjJ2dDBZTVEwbFVQZnB0cWR1c1dwZEdqa3djU3h2d2UtSkpCX2NkSWRZVWhacG5JcHFZU0J3dUkxb1AzQ05SRWktcFZJd1RoZEp4Y3Ro?oc=5) (`전기신문`, 11/25 15:41)
  - 🇰🇷 [440. 자율주행도 피지컬 AI와 생성형 AI 주도로 판이 바뀌었다.](https://news.google.com/rss/articles/CBMickFVX3lxTE5vd01vU2V0cTBULWViREV3Qm9TR3lZUEdqYm5UdjdqQXlWR1hmRkIyS0JCOUtWeEN1RlpmM2hyc1ZWYnBWN0VVbHlCS2hHTkxFLVF0Q2FPYUNhQ3hTYm1JZkpESHZiLVBYc2VpVTk2c1BZZw?oc=5) (`다나와 자동차`, 11/24 17:02)
  - 🌐 [An Eric Trump-backed startup unveils a powerful new humanoid robot—and won't rule out arming it](https://news.google.com/rss/articles/CBMijAFBVV95cUxOay05N1JJSXFwUk1VakFZM3ZXRVVsSkEyWVhiSlVoUmt2b2c5bzJCcEx5cGE3WU5qbktYemF5WVBPZFlsMTd0NmJCM3ZNSnhBYndUblI1SHBvNTdNR0d0ZWNzS0xJOVNTS0hFZ3NoY05ialAwUHdLdlozNU5XbDl4ek05VlV4UWJQRDdvTw?oc=5) (`Fast Company`, 11/18 22:58)
  - 🌐 [Visions of Japan overrun by humanoid robot imports inspire startups](https://news.google.com/rss/articles/CBMihAFBVV95cUxOSVI5NG1kS0VuZ3ZXaFBiM0hDZm9aRGt4bWY0aWFSc3Q5c0hob2tWUnBBcWZPbkpzcktXVVBid3UzMVZ6MnlUOExnaVhrcHRKR01GQlV5OTdaMmEyS3ZSQ1RtcXNzcHdFZWJfUy1kT0hYU21lczE4Y0RtRVJvMUlDMmJwV1k?oc=5) (`The Japan Times`, 11/23 14:18)

---

## ⚡ 파트 2. 주간 IT · AI 주요 단신 8선 (Quick Radar)

| 번호 | 분야 | 핵심 단신 헤드라인 (원문 링크) | 출처 · 시각 |
| :---: | :---: | :--- | :---: |
| **01** | `오픈 웨이트·AI엔지니어링` | **[사이오닉에이아이, LLM 게이트웨이 출시...오픈웨이트 모델 성능 최적화해 제공](https://news.google.com/rss/articles/CBMic0FVX3lxTE5UbTNoSDJyQWJsQ0ZGYWhRUnhfQno5aDZJM2N0eVFYWXRFdXVYeGc5dUtHRTV3Ym1EUmc5dVpEQ1lmdjViVWw0RWg4UkxJbEN4YTBVV1ZzeXNNZ3lWOXJ3SVl3djNBNFJ1RjZkYklIVkdiTzA?oc=5)** | `디지털투데이` (11/24 09:58) |
| **02** | `스타트업·VC` | **[[유미's 픽] 앤트로픽에 돈 몰리는데…IPO 앞둔 업스테이지, 자금 확보 '고심'](https://news.google.com/rss/articles/CBMiVkFVX3lxTE9pNU12a3BHWlQ0YTR1MW5mTDBfdWhvSmR5RUZHN0I4emdBa09wcHdSTU91Njl6V3pxaFZ0a0tsdW9UWjJaQ0x0RlZ1OUpRTTBlNkt1Wmt3?oc=5)** | `지디넷코리아` (11/20 10:41) |
| **03** | `국내 AI·빅테크` | **[[단독] 통신3사·네이버, AI 에이전트 전화 응대 거부키로](https://news.google.com/rss/articles/CBMigwFBVV95cUxQQnQ1dzJXeUxDSTJwQV9rSEhMQ0RRSDZZczZVbXBMaGxpQlBtQk4wVnJyc1ZsbEhoM0xzUVNuRWhYaDNxa3JKaFY4bm5ZM2ZmMUtvRWV5TGtVbFlYQVloYnVTVTBwdjRFZ09qYXBvTkpIOVhZbE4zbWI1cGVacjh2TVlLOA?oc=5)** | `조선일보` (11/23 14:35) |
| **04** | `디바이스·온디바이스` | **[인터넷 연결 안 하고 커닝…내년 ‘온디바이스AI’ 주의보](https://news.google.com/rss/articles/CBMiWkFVX3lxTFA5WEtzdFJQc1EtQ1FMNDZubzRLTHdqUFBhLTVpZDRYaWc0Sk9hNi15ZkRmdWhUOGRCeDdvR01iYVlSX25iMjg0YWhPdEZuT2dnYzVXUlluOGljZ9IBX0FVX3lxTE1iM3E5VWFWWkJIRHR3WnBqNk5uQ0dmLURQTFBrbUVuek1OOURXVk9iV2FjQlNySXNnQmpNMjNfaVByRUwxM0d3ODcwUG9MOVMwZ1UyYVRRaG5HZ1RyRWpF?oc=5)** | `경향신문` (11/22 21:08) |
| **05** | `클라우드·데이터` | **[[AI 고속도로] 엔비디아가 돈 대고 GPU 팔고…네오클라우드 '순환 투자' 시험대](https://news.google.com/rss/articles/CBMiVkFVX3lxTFB1OHJOUDY0WElKci14SGU0bW0waFk2eGJwTHRuZnZOaGxyZXMwNURjSkpzVEJUZ0hwbUQza3BPVzJFSFNkQk1vVGRGSFdRRjdma09kMmdB?oc=5)** | `지디넷코리아` (11/20 09:40) |
| **06** | `사이버보안` | **[AI 에이전트도 해킹 표적 된다…포티넷이 전망한 2027년 보안 위협](https://news.google.com/rss/articles/CBMibEFVX3lxTE5HbnI2SjhvLTZ3c01YREM3alNKN0VDYW9mLWRHSkdCYi0zWmxXRE5EWE82cHhtYTFIZm9wV1kyRTVLNTN3QlQ5aFVoMnBCWUQteWY1N05FVFY5VFJjeEVia1RobUt1dkJET0FRUA?oc=5)** | `뉴스탭` (11/25 09:11) |
| **07** | `로보틱스·모빌리티` | **[일론 머스크 "AI칩 AI5, 테슬라 FSD보다 옵티머스에 우선 적용"](https://news.google.com/rss/articles/CBMiY0FVX3lxTE4xSm9fa1F0VW5XZ0t4YWZfTno4N0NJUVNESDdYRS1xblUyeHk5b1BoZHB5cnpJbEZTa29OOTlFVGt6cXRTZ0hpSm00QXVBUV9CMWVHMUVZX0FNNEpYbW1JR0Z6WQ?oc=5)** | `더구루` (11/23 13:18) |
| **08** | `AI 정책·저작권` | **[미 행정부, 중국 AI 막으려 기업들 ‘이름 공개 망신주기’ 검토... 중국AI 쓰면 홈페이지에 밝혀라](https://news.google.com/rss/articles/CBMigwFBVV95cUxQUXZVSVBaUExPS3lxUUJtbkVaTmhCSi1uTWVfRFp3Z21NdjM1Tm1wMHkwZGozOVRCNFV6SWtwMExfclZTVjNoSnNxazF4UjdIT0w5VHVEXzhsRzV3SldBMWpWZGVwREFNUnlnN09IeWd2d2NYWVdQMGMzcmltVGFjODRJVQ?oc=5)** | `조선일보` (11/19 15:25) |

---

## 🌐 파트 3. 글로벌 1차 테크 · 오픈 웨이트 피드 (Hugging Face · VentureBeat · Simon Willison · TechCrunch 등)

- **[Hugging Face Blog]** [Microduck Obstacle Avoidance: A Sim2Real Workflow with Isaac Lab and Newton](https://huggingface.co/blog/nvidia/microduck-obstacle-avoidance) (11/25 01:34)
- **[Hugging Face Blog]** [RoboTrack: Point tracking for real-world robotic manipulation](https://huggingface.co/blog/allenai/robotrack) (11/24 02:20)
- **[Hugging Face Blog]** [How to build and maintain an agentic evaluation](https://huggingface.co/blog/agentic-evals) (11/23 09:00)
- **[Simon Willison AI]** [Three LLM inflection points in twelve months](https://simonwillison.net/2026/Nov/24/llm-inflection-points/) (2026-11-24)
- **[Simon Willison AI]** [GPT 6.2 Astra Solves a Historical Mystery](https://simonwillison.net/2026/Nov/24/astra-historical-mystery/) (2026-11-24)
- **[Simon Willison AI]** [datasette-charts 0.2a0](https://simonwillison.net/2026/Nov/24/datasette-charts/) (2026-11-24)
- **[TechCrunch AI]** [Yale’s Sonnenfeld: Nvidia is a ‘detriment’ to US industrial might — not a champion](https://techcrunch.com/2026/11/24/yales-sonnenfeld-nvidia-is-a-detriment-to-u-s-industrial-might-not-a-champion/) (11/25 09:12)
- **[TechCrunch AI]** [Jensen Huang still thinks a succession plan creates unnecessary hierarchy](https://techcrunch.com/2026/11/24/jensen-huang-still-thinks-a-succession-plan-creates-unnecessary-hierarchy/) (11/25 07:27)
- **[TechCrunch AI]** [In all-hands meeting, Jensen Huang thanks White House and says he’s in therapy](https://techcrunch.com/2026/11/24/in-all-hands-meeting-jensen-huang-thanks-white-house-and-says-hes-in-therapy/) (11/25 06:48)
- **[The Verge AI]** [Jensen Huang reportedly tells Nvidia staff it’s ‘not true’ Trump got him rehired](https://www.theverge.com/tech/1041571/jensen-huang-all-hands-nvidia-apology) (2026-11-24)
- **[The Verge AI]** [David Fincher is being dragged for suspected use of AI in his latest film](https://www.theverge.com/entertainment/1041417/david-fincher-netflix-cliff-booth-ai-interpositive) (2026-11-24)
- **[The Verge AI]** [Tidal will start banning AI-generated music next month](https://www.theverge.com/entertainment/1041362/tidal-ai-music-ban) (2026-11-24)

---

## 💬 Slack 복붙용 포스팅 초안

```text
🤖 *[주간 IT · AI 핵심 브리핑]* (2026.11.18 ~ 2026.11.25)
이번 주 글로벌·국내 IT·AI 핵심 4대 이슈를 3분 영상으로 정리했습니다. 🎬

*📌 이번 주 4대 핵심 이슈*
• *[AI 모델 · 에이전트 · 오픈 웨이트]* Thinking Machines Lab, 오픈 웨이트 'Inkling 2 Mini' 및 학습 API 'Tinker · Tinker Cookbook' 생태계 공개
• *[AI 반도체 · 인프라]* 전력반도체 시장 규모, 2031년 92조원…AI·로봇이 성장 이끌어 (전자신문)
• *[빅테크 · 클라우드 · SaaS]* AI 투자 안해서 웃었다? 애플, 엔비디아 ‘시총 왕좌’ 뺏었다 (중앙일보)
• *[피지컬 AI · 보안 · 테크 정책]* AI·로봇이 바꾸는 건설현장…25일부터 스마트건설 엑스포 (연합뉴스)

*⚡ 주간 단신 레이더 TOP 4*
• `오픈 웨이트·AI엔지니어링` 사이오닉에이아이, LLM 게이트웨이 출시...오픈웨이트 모델 성능 최적화해 제공
• `스타트업·VC` [유미's 픽] 앤트로픽에 돈 몰리는데…IPO 앞둔 업스테이지, 자금 확보 '고심'
• `국내 AI·빅테크` [단독] 통신3사·네이버, AI 에이전트 전화 응대 거부키로
• `디바이스·온디바이스` 인터넷 연결 안 하고 커닝…내년 ‘온디바이스AI’ 주의보

📊 슬라이드 원본: https://docs.google.com/presentation/d/1yad5aoY8SAX-fImKETc520AsWWwWwPvWojVLGJTKQ68/edit
📁 주간 브리핑 아카이브: https://drive.google.com/drive/folders/1wiIpcQGPbBwOqu9t_JxJg2C9LOhQSa60
```

## 🎬 영상 제작 & Slack 발행 가이드 (3분 컷)
1. **Antigravity** 채팅창에 **`"이번 주 IT·AI 브리핑 슬라이드 만들어줘"`** 입력 → 우측 하단 아바타 PiP · 하단 자막 Safe Zone이 반영된 **8장 Google Slides + 방송 대본(발표자 노트)** 자동 생성
2. Google Slides에서 **`파일 → 동영상으로 변환 (Google Vids)`** 클릭 → **`발표자 노트로 대체`** 선택
3. 8장 전 슬라이드 우측 하단에 **한국어 AI 아바타** 배치 + 우측 사이드바 **`Captions(스타일 자막)`** 전체 적용 → **MP4 다운로드**
4. MP4 + 위 Slack 복붙 텍스트를 Slack 채널에 업로드 완료!
