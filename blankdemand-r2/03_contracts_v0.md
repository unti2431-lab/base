# contracts_v0 — 레인 공통 계약 (발행: L0, 2026-10-08)

> 이 파일이 바뀌면 버전을 올린다(v0 → v1). 레인은 HANDOFF에 사용한 계약 버전을 적는다.
> [추정] 표시는 실제 파일 로드 후 L2가 확인해 v1에서 확정한다.

---

## C1. 원천 데이터 스키마 (FreshRetailNet-50K, 1행 = 시계열 1개 × 1일)

| 필드 | 형 | 의미 | 비고 |
|---|---|---|---|
| `city_id`, `store_id`, `management_group_id` | int | 지역·점포·관리그룹 | |
| `first_category_id`, `second_category_id`, `third_category_id` | int | 상품 분류 | |
| `product_id` | int | 상품 | 시계열 키 = (`store_id`, `product_id`) |
| `dt` | date | 날짜 | |
| `sale_amount` | float | 일 판매(정규화) | 실제 개수 아님 |
| `hours_sale` | float[24] | 시간대 판매 | 합 = `sale_amount` 인지 E3로 검사 |
| `stock_hour6_22_cnt` | int | 06–22시 품절 시간 수 | > 0 이면 품절 영향일 |
| `hours_stock_status` | int[24] | 시간대 품절 플래그 | [추정] 1 = 품절. L2가 `stock_hour6_22_cnt`와 대조해 확정 |
| `discount` | float | 1.0 = 할인 없음, 0.9 = 10% 할인 | |
| `holiday_flag`, `activity_flag` | int | 휴일·행사 표시 | |
| `precpt`, `avg_temperature`, `avg_humidity`, `avg_wind_level` | float | 실측 기상 | 당일값 사용 금지 |

분할: train 4,500,000행(90일) / eval 350,000행(7일). [추정] eval = 2024-06-26 ~ 07-02.

## C2. 특성 시점표 (누수 방지)

| 등급 | 필드 | 발주 판단 시점(D-1 마감)에서 D일 예측에 쓸 수 있는 값 |
|---|---|---|
| A 사전 확정 | `dt`의 요일, `holiday_flag` | D일 값 사용 가능 |
| B 계획 변수 | `discount`, `activity_flag` | **v0: D-1까지 값만.** 사전 계획값으로 볼 근거가 확인되면 v1에서 A로 승격 |
| C 사후 관측 | `sale_amount`, `hours_sale`, `hours_stock_status`, `stock_hour6_22_cnt`, 기상 4종 | D-1까지만 |

## C3. 영업창

- 기본 영업창: **06:00–22:00** (hour index 6~21). 창 밖 시간은 품절 플래그가 있어도 수요 복원 대상 아님.
- "완전 관측일" = 영업창 안 품절 시간 0.

## C4. 표본·분할 매니페스트

```json
// data/manifest/split.json
{
  "contract": "v0",
  "source": {"repo": "Dingdong-Inc/FreshRetailNet-50K", "revision": "<commit or date>", "files": {"train.parquet": "<sha256>", "eval.parquet": "<sha256>"}},
  "train_days": ["YYYY-MM-DD", "YYYY-MM-DD"],   // 앞 56일
  "valid_days": ["YYYY-MM-DD", "YYYY-MM-DD"],   // 다음 14일
  "lock_days":  ["YYYY-MM-DD", "YYYY-MM-DD"],   // 마지막 20일 — 10/16 전까지 읽기 금지
  "official_eval_days": ["YYYY-MM-DD", "YYYY-MM-DD"],
  "sample": {"seed": 20261008, "strata": "stockout_ratio_tercile x mean_sale_tercile", "n": 200, "ids_file": "sample_ids_200.csv"}
}
```

## C5. 판정 출력 (L3 → L4 → L5 공통)

```json
// 실행 1회 = 파일 1개: runs/<run_id>/decisions.json
{
  "contract": "v0",
  "run_id": "20261010T1530_W_r2",
  "versions": {"data": "<split.json sha>", "code": "<git short sha>", "rules": "rules_v0", "packages": "requirements.lock sha"},
  "cost": {"ratio_under_over": 2, "tau": 0.6667},
  "rows": [
    {
      "row_id": "s{store_id}_p{product_id}_{D}",
      "decision_date": "YYYY-MM-DD",
      "status": "KEEP | REVIEW | HOLD | INPUT_ERROR",
      "existing_plan": {"value": 0.0, "source": "user | B0"},
      "alternative": {"value": 0.0, "method": "B2 | W | P1 | P2"},
      "unit": "normalized",
      "observed_vs_estimated": {"observed_sales_lastday": 0.0, "estimated_demand_lastday": 0.0, "estimated": true},
      "uncertainty": {"p10": 0.0, "p50": 0.0, "p90": 0.0, "dominance_ratio": 0.0},
      "rule_hits": ["H2", "R2"],
      "evidence": ["사람이 읽는 근거 문장 — 템플릿 생성, LLM 자유문장 금지"],
      "unchecked": ["포장 단위", "현재 재고"],
      "next_action": "다음 확인 행동(HOLD/INPUT_ERROR일 때 필수)"
    }
  ]
}
```

- 상태 코드 ↔ 화면 표기: KEEP=기존안 유지, REVIEW=수정 검토, HOLD=추천 보류, INPUT_ERROR=입력 오류.
- 판정 규칙 ID(E1~E3, H1~H3, M1, K0, R1, R2)는 `01_review_R2.1.md` §3과 동일.

## C6. 평가 출력

`runs/<run_id>/metrics.csv` — 열: `method, cost_ratio, split, n_rows, n_full_obs_days, rel_cost_full_obs, sure_shortfall_lb, hold_rate, mixed_policy_cost, mask_type(realistic|random)`

## C7. 실패시험 12종 v0 (R2 원 명세가 있으면 그 번호를 우선)

| ID | 시험 | 기대 |
|---|---|---|
| T01 | 필수 필드 누락 | INPUT_ERROR(E1) |
| T02 | 음수 판매 | INPUT_ERROR(E1) |
| T03 | 24시간 배열 길이 오류 | INPUT_ERROR(E1) |
| T04 | 일 합 ≠ 시간대 합 | INPUT_ERROR(E3) |
| T05 | D일 실측 기상이 특성에 포함 | INPUT_ERROR(E2) |
| T06 | D일 판매·품절 플래그 혼입 | INPUT_ERROR(E2) |
| T07 | 완전 재고·판매 0 (정상 0) | 보정 없음(R1), 위반 시 실패 |
| T08 | 품절일 대안 < 관측 판매 | R2 경고 표시 |
| T09 | 최근 14일 완전 관측일 < 3 | HOLD(H1) |
| T10 | Σp_h < 0.3 (재고 정상 시간이 거의 없음) | HOLD(H2) |
| T11 | 단위 필드 불명/혼합 | HOLD 또는 INPUT_ERROR, 숫자 생성 금지 |
| T12 | 입력 1개 변경 | 캐시 키 변경 + 재계산, 결과 파일 해시 변경 |

## C8. STATUS.md 형식 (L0 전용)

```
# STATUS — YYYY-MM-DD HH:MM / 계약 vN / 다음 관문 G?
| 레인 | 현재 카드 | 상태(진행/대기/막힘/완료) | 최신 HANDOFF | 막힌 이유 |
| 관문 체크 | 조건 | 증거 파일 | 충족? |
| 미해결 결정 (사람) | ... |
| 다음 라운드 카드 요약 | ... |
```
