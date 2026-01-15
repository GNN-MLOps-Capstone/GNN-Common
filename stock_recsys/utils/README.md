# 📊 Sentiment Calculator

종목 및 키워드별 감성 지수 계산 라이브러리

---

## ✨ 주요 기능

- ✅ **종목별 감성 지수 계산**: 뉴스 데이터 기반 종목별 감성 분석
- ✅ **키워드별 감성 지수 계산**: 키워드별 긍정/부정 감성 집계
- ✅ **시간 가중치 적용**: 최근 뉴스에 더 높은 가중치 부여
- ✅ **최종 추천 점수 계산**: 키워드 연관성 + 감성 지수 결합
- ✅ **다양한 출력 형식**: List, DataFrame, CSV 지원

---

## 🚀 빠른 시작

### 설치

```python
# sentiment_calculator.py 파일을 프로젝트에 복사
cp sentiment_calculator.py your_project/utils/
```

### 기본 사용

```python
from utils.sentiment_calculator import SentimentCalculator
import pandas as pd

# 데이터 로드
df = pd.read_csv('data/sentiment/keyword_sentiment.csv')

# 계산기 생성
calculator = SentimentCalculator()

# 종목별 감성 지수 계산
stock_results = calculator.calculate_stock_sentiment(
    df, 
    stock_col='related_stocks',
    sentiment_col='stocks_sentiment_str'
)

# 결과 출력
calculator.print_results(stock_results, result_type='stock')

# DataFrame으로 저장
stock_df = calculator.to_dataframe(stock_results, add_grade=True)
stock_df.to_csv('stock_sentiment_index.csv', index=False)
```

---

## 📖 API 문서

### SentimentCalculator 클래스

#### 초기화

```python
calculator = SentimentCalculator(decay_rate=0.1)
```

**Parameters:**
- `decay_rate` (float): 시간 가중치 감쇠율 (기본값: 0.1 = 하루당 10% 감소)

---

#### calculate_stock_sentiment()

종목별 감성 지수 계산

```python
stock_results = calculator.calculate_stock_sentiment(
    df,
    stock_col='related_stocks',
    sentiment_col='stocks_sentiment_str',
    split_comma=True
)
```

**Parameters:**
- `df` (pd.DataFrame): 뉴스 데이터프레임
- `stock_col` (str): 종목 컬럼명
- `sentiment_col` (str): 감성 컬럼명
- `split_comma` (bool): 컴마로 종목 분리 여부 (기본값: True)

**Returns:**
- `List[Dict]`: 종목별 결과
  ```python
  [{
      'stock': '삼성전자',
      'total': 10,
      'positive': 8,
      'negative': 1,
      'neutral': 1,
      'sentiment_index': 0.7
  }, ...]
  ```

---

#### calculate_keyword_sentiment()

키워드별 감성 지수 계산

```python
keyword_results = calculator.calculate_keyword_sentiment(
    df,
    keyword_col='keywords',
    keyword_sentiment_col='keywords_sentiment_str'
)
```

**Parameters:**
- `df` (pd.DataFrame): 뉴스 데이터프레임
- `keyword_col` (str): 키워드 컬럼명
- `keyword_sentiment_col` (str): 키워드 감성 컬럼명

**Returns:**
- `List[Dict]`: 키워드별 결과

---

#### calculate_weighted_sentiment()

시간 가중치를 적용한 종목별 감성 지수 계산

```python
weighted_results = calculator.calculate_weighted_sentiment(
    df,
    stock_col='related_stocks',
    sentiment_col='stocks_sentiment_str',
    date_col='pub_date',
    split_comma=True
)
```

**Parameters:**
- `df` (pd.DataFrame): 뉴스 데이터프레임
- `stock_col` (str): 종목 컬럼명
- `sentiment_col` (str): 감성 컬럼명
- `date_col` (str): 날짜 컬럼명
- `split_comma` (bool): 컴마로 종목 분리 여부

**Returns:**
- `List[Dict]`: 종목별 결과 (일반 감성지수 + 가중 감성지수)
  ```python
  [{
      'stock': '삼성전자',
      'total': 10,
      'positive': 8,
      'negative': 1,
      'neutral': 1,
      'sentiment_index': 0.7,
      'weighted_sentiment_index': 0.75,  # 시간 가중치 적용
      'avg_weight': 0.85
  }, ...]
  ```

---

#### to_dataframe()

결과를 DataFrame으로 변환

```python
df = calculator.to_dataframe(results, add_grade=True)
```

**Parameters:**
- `results` (List[Dict]): calculate 메서드의 반환값
- `add_grade` (bool): 등급 컬럼 추가 여부 (기본값: True)

**Returns:**
- `pd.DataFrame`: 결과 데이터프레임

---

#### print_results()

결과를 표 형식으로 출력

```python
calculator.print_results(results, result_type='stock')
```

**Parameters:**
- `results` (List[Dict]): calculate 메서드의 반환값
- `result_type` (str): 'stock' 또는 'keyword'

---

### 유틸리티 함수

#### calculate_final_recommendation_score()

최종 추천 점수 계산

```python
from utils.sentiment_calculator import calculate_final_recommendation_score

final_score = calculate_final_recommendation_score(
    keyword_relevance=9.5,  # 0~10
    sentiment_index=0.8     # -1.0 ~ +1.0
)
# 결과: 89.0 (0~100)
```

**공식:**
```
최종 점수 = (키워드 연관성 × 6.0) + (감성 지수 × 40)
         = (키워드 점수 × 60%) + (감성 점수 × 40%)
```

---

## 📊 감성 지수 계산 공식

### 기본 감성 지수

```
감성 지수 = (긍정 뉴스 수 - 부정 뉴스 수) / 전체 뉴스 수
```

**범위:** -1.0 ~ +1.0
- `+1.0`: 모든 뉴스가 긍정 (매우 긍정적)
- `+0.5`: 긍정이 많음 (긍정적)
- `0.0`: 긍정과 부정이 같음 (중립)
- `-0.5`: 부정이 많음 (부정적)
- `-1.0`: 모든 뉴스가 부정 (매우 부정적)

---

### 시간 가중 감성 지수

```
가중 감성 지수 = Σ(감성 점수 × 시간 가중치) / Σ(시간 가중치)
```

**시간 가중치:**
```
가중치 = max(0.3, 1.0 - days_diff × decay_rate)
```

**예시 (decay_rate=0.1):**
- 당일 뉴스: 가중치 1.0
- 1일 전: 가중치 0.9
- 2일 전: 가중치 0.8
- 3일 전: 가중치 0.7
- 7일 이상: 가중치 0.3 (최소값)

---

## 🎯 등급 기준

| 감성 지수 | 등급 | 설명 |
|-----------|------|------|
| +0.5 ~ +1.0 | 매우 긍정적 | 대부분의 뉴스가 긍정적 |
| +0.2 ~ +0.5 | 긍정적 | 긍정 뉴스가 많음 |
| -0.2 ~ +0.2 | 중립적 | 긍정과 부정이 비슷 |
| -0.5 ~ -0.2 | 부정적 | 부정 뉴스가 많음 |
| -1.0 ~ -0.5 | 매우 부정적 | 대부분의 뉴스가 부정적 |

---

## 💡 사용 예시

### 예시 1: 종목별 감성 분석

```python
calculator = SentimentCalculator()

# 종목별 감성 지수 계산
stock_results = calculator.calculate_stock_sentiment(
    df, 'related_stocks', 'stocks_sentiment_str'
)

# 상위 5개 출력
for rank, r in enumerate(stock_results[:5], 1):
    print(f"{rank}. {r['stock']}: {r['sentiment_index']:+.3f}")
```

**출력:**
```
1. KB금융: +1.000
2. 안랩: +1.000
3. 삼성전자: +0.750
4. 현대차: +0.000
5. KT: -1.000
```

---

### 예시 2: 시간 가중치 비교

```python
calculator = SentimentCalculator(decay_rate=0.1)

weighted_results = calculator.calculate_weighted_sentiment(
    df, 'related_stocks', 'stocks_sentiment_str', 'pub_date'
)

# 일반 vs 가중 감성 지수 비교
for r in weighted_results[:5]:
    print(f"{r['stock']:<15} | 일반: {r['sentiment_index']:+.3f} | "
          f"가중: {r['weighted_sentiment_index']:+.3f} | "
          f"차이: {r['weighted_sentiment_index'] - r['sentiment_index']:+.3f}")
```

**출력:**
```
KB금융          | 일반: +1.000 | 가중: +0.950 | 차이: -0.050
삼성전자        | 일반: +0.750 | 가중: +0.820 | 차이: +0.070
현대차          | 일반: +0.000 | 가중: -0.200 | 차이: -0.200
```

---

### 예시 3: 최종 추천 점수 계산

```python
# 삼성전자: 키워드 "AI 반도체" 연관성 9.5, 감성 지수 +0.8
score = calculate_final_recommendation_score(9.5, 0.8)
print(f"최종 추천 점수: {score:.1f}/100")
# 결과: 89.0/100 (강력 추천!)

# 현대차: 키워드 "전기차" 연관성 8.0, 감성 지수 -0.3
score = calculate_final_recommendation_score(8.0, -0.3)
print(f"최종 추천 점수: {score:.1f}/100")
# 결과: 36.0/100 (주의)
```

---

## 📁 파일 구조

```
stock_recsys/
├── utils/
│   └── sentiment_calculator.py  # 라이브러리 파일
├── data/
│   └── sentiment/
│       ├── keyword_sentiment.csv  # 입력 데이터
│       ├── stock_sentiment_index.csv  # 출력 (종목별)
│       ├── keyword_sentiment_index.csv  # 출력 (키워드별)
│       └── weighted_sentiment_index.csv  # 출력 (시간 가중)
└── notebooks/
    └── sentiment_analysis.ipynb  # 사용 예시
```

---

## 🔧 요구사항

```
pandas >= 1.0.0
numpy >= 1.18.0
python >= 3.7
```
