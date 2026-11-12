# Lite 독립 이관 작업 브랜치 (2026-11-12 KST)

## 계약
- 소스: `hibi89/REA_Web@feature/lite-owner-delivery-p95-20261112` 검증 기능 SHA `cb7df1f4d1ce517c5940570af5bb1085410de268`.
- 원본에서 **허용된 기능 계약만** 가져오고 Pro FastAPI/SQLite·Fable/Astra import 전체 복제 금지. README/LICENSE/NOTICE/원본 blob SHA 기록.
- 첫 목표: 독립 CSV/flat JSON parser → 명시 mapping/sha/owner APPROVE → 단일 HTML → create-only ZIP/verifier → 브라우저 file:// 열기, 저장, 재열기.
- 합성 goldens, malformed CSV/JSON, XSS/PII/no-network/no-clobber, dual Windows/Ubuntu CI 전부 exact SHA 근거.
- 기존 REA_Web 원본과 신규 저장소 소스/고객 데이터 별도 유지. 권리/실사용 고객/유료 납품 HOLD.
- **신규 독립 소스 아직 미이관**, 제품 전체 최종률 UNASSESSED, 구현 검증률 0. 최초 50% 게이트를 새 저장소 실 E2E로 판단.
