"""
종목 및 키워드별 감성 지수 계산 라이브러리

사용 예시:
    from sentiment_calculator import SentimentCalculator
    
    calculator = SentimentCalculator()
    
    # 종목별 감성 지수 계산
    stock_results = calculator.calculate_stock_sentiment(
        df, 
        stock_col='related_stocks',
        sentiment_col='stocks_sentiment_str'
    )
    
    # 키워드별 감성 지수 계산
    keyword_results = calculator.calculate_keyword_sentiment(
        df,
        keyword_col='keywords',
        keyword_sentiment_col='keywords_sentiment_str'
    )
    
    # 시간 가중치 적용
    weighted_results = calculator.calculate_weighted_sentiment(
        df,
        stock_col='related_stocks',
        sentiment_col='stocks_sentiment_str',
        date_col='pub_date'
    )
"""

import pandas as pd
import numpy as np
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Tuple, Optional


class SentimentCalculator:
    """종목 및 키워드별 감성 지수 계산기"""
    
    def __init__(self, decay_rate: float = 0.1):
        """
        초기화
        
        Args:
            decay_rate: 시간 가중치 감쇠율 (기본 0.1 = 하루당 10% 감소)
        """
        self.decay_rate = decay_rate
    
    @staticmethod
    def sentiment_to_score(sentiment: str) -> float:
        """
        감성 라벨을 점수로 변환
        
        Args:
            sentiment: 감성 라벨 (긍정/부정/중립)
            
        Returns:
            float: 감성 점수 (+1.0, -1.0, 0.0)
        """
        sentiment = str(sentiment).strip()
        if '긍정' in sentiment:
            return 1.0
        elif '부정' in sentiment:
            return -1.0
        else:
            return 0.0
    
    @staticmethod
    def calculate_sentiment_index(positive: int, negative: int, total: int) -> float:
        """
        감성 지수 계산
        
        공식: (긍정 - 부정) / 전체
        
        Args:
            positive: 긍정 개수
            negative: 부정 개수
            total: 전체 개수
            
        Returns:
            float: 감성 지수 (-1.0 ~ +1.0)
        """
        if total == 0:
            return 0.0
        return (positive - negative) / total
    
    def calculate_time_weight(self, pub_date, reference_date: Optional[datetime] = None) -> float:
        """
        시간 가중치 계산
        
        Args:
            pub_date: 발행일 (datetime 또는 문자열)
            reference_date: 기준일 (None이면 오늘)
            
        Returns:
            float: 시간 가중치 (0.3 ~ 1.0)
        """
        if reference_date is None:
            reference_date = datetime.now()
        
        # 문자열이면 datetime으로 변환
        if isinstance(pub_date, str):
            try:
                for fmt in ['%Y/%m/%d %H:%M', '%Y-%m-%d %H:%M', '%Y/%m/%d', '%Y-%m-%d']:
                    try:
                        pub_date = datetime.strptime(pub_date, fmt)
                        break
                    except ValueError:
                        continue
            except:
                return 1.0
        
        # 날짜 차이 계산
        days_diff = (reference_date - pub_date).days
        
        if days_diff < 0:
            return 1.0
        
        # 시간 가중치: 최소 0.3까지만 감소
        weight = max(0.3, 1.0 - days_diff * self.decay_rate)
        return weight
    
    def calculate_stock_sentiment(
        self,
        df: pd.DataFrame,
        stock_col: str = 'related_stocks',
        sentiment_col: str = 'stocks_sentiment_str',
        split_comma: bool = True
    ) -> List[Dict]:
        """
        종목별 감성 지수 계산
        
        Args:
            df: 뉴스 데이터프레임
            stock_col: 종목 컬럼명
            sentiment_col: 감성 컬럼명
            split_comma: 컴마로 종목 분리 여부
            
        Returns:
            list: 종목별 결과 (감성 지수 포함)
        """
        stock_data = defaultdict(lambda: {
            'positive': 0,
            'negative': 0,
            'neutral': 0,
            'total': 0
        })
        
        for _, row in df.iterrows():
            stock_str = str(row[stock_col]).strip()
            sentiment = str(row[sentiment_col]).strip()
            
            if stock_str and stock_str != 'nan' and stock_str != '':
                # 컴마 분리
                if split_comma:
                    stocks = [s.strip() for s in stock_str.split(',')]
                else:
                    stocks = [stock_str]
                
                # 각 종목별로 집계
                for stock in stocks:
                    if stock:
                        stock_data[stock]['total'] += 1
                        
                        if '긍정' in sentiment:
                            stock_data[stock]['positive'] += 1
                        elif '부정' in sentiment:
                            stock_data[stock]['negative'] += 1
                        else:
                            stock_data[stock]['neutral'] += 1
        
        # 감성 지수 계산
        results = []
        for stock, data in stock_data.items():
            sentiment_index = self.calculate_sentiment_index(
                data['positive'], data['negative'], data['total']
            )
            results.append({
                'stock': stock,
                'total': data['total'],
                'positive': data['positive'],
                'negative': data['negative'],
                'neutral': data['neutral'],
                'sentiment_index': sentiment_index
            })
        
        return sorted(results, key=lambda x: x['sentiment_index'], reverse=True)
    
    def calculate_keyword_sentiment(
        self,
        df: pd.DataFrame,
        keyword_col: str = 'keywords',
        keyword_sentiment_col: str = 'keywords_sentiment_str'
    ) -> List[Dict]:
        """
        키워드별 감성 지수 계산
        
        Args:
            df: 뉴스 데이터프레임
            keyword_col: 키워드 컬럼명
            keyword_sentiment_col: 키워드 감성 컬럼명
            
        Returns:
            list: 키워드별 결과 (감성 지수 포함)
        """
        keyword_data = defaultdict(lambda: {
            'positive': 0,
            'negative': 0,
            'neutral': 0,
            'total': 0
        })
        
        for _, row in df.iterrows():
            keywords_str = str(row[keyword_col]).strip()
            keyword_sentiment = str(row[keyword_sentiment_col]).strip()
            
            if keywords_str and keywords_str != 'nan' and keywords_str != '':
                keywords = [s.strip() for s in keywords_str.split(',')]
                keyword_sentiments = [s.strip() for s in keyword_sentiment.split(',')]
                
                for keyword, sentiment in zip(keywords, keyword_sentiments):
                    if keyword:
                        keyword_data[keyword]['total'] += 1
                        
                        if '긍정' in sentiment:
                            keyword_data[keyword]['positive'] += 1
                        elif '부정' in sentiment:
                            keyword_data[keyword]['negative'] += 1
                        else:
                            keyword_data[keyword]['neutral'] += 1
        
        # 감성 지수 계산
        results = []
        for keyword, data in keyword_data.items():
            sentiment_index = self.calculate_sentiment_index(
                data['positive'], data['negative'], data['total']
            )
            results.append({
                'keyword': keyword,
                'total': data['total'],
                'positive': data['positive'],
                'negative': data['negative'],
                'neutral': data['neutral'],
                'sentiment_index': sentiment_index
            })
        
        return sorted(results, key=lambda x: x['sentiment_index'], reverse=True)
    
    def calculate_weighted_sentiment(
        self,
        df: pd.DataFrame,
        stock_col: str = 'related_stocks',
        sentiment_col: str = 'stocks_sentiment_str',
        date_col: str = 'pub_date',
        split_comma: bool = True
    ) -> List[Dict]:
        """
        시간 가중치를 적용한 종목별 감성 지수 계산
        
        Args:
            df: 뉴스 데이터프레임
            stock_col: 종목 컬럼명
            sentiment_col: 감성 컬럼명
            date_col: 날짜 컬럼명
            split_comma: 컴마로 종목 분리 여부
            
        Returns:
            list: 종목별 결과 (일반 감성지수 + 가중 감성지수)
        """
        stock_data = defaultdict(lambda: {
            'positive': 0,
            'negative': 0,
            'neutral': 0,
            'total': 0,
            'weighted_scores': [],
            'weights': []
        })
        
        for _, row in df.iterrows():
            stock_str = str(row[stock_col]).strip()
            sentiment = str(row[sentiment_col]).strip()
            pub_date = row[date_col]
            
            if stock_str and stock_str != 'nan' and stock_str != '':
                # 컴마 분리
                if split_comma:
                    stocks = [s.strip() for s in stock_str.split(',')]
                else:
                    stocks = [stock_str]
                
                # 시간 가중치 계산
                time_weight = self.calculate_time_weight(pub_date)
                
                # 감성 점수
                if '긍정' in sentiment:
                    sentiment_score = 1.0
                elif '부정' in sentiment:
                    sentiment_score = -1.0
                else:
                    sentiment_score = 0.0
                
                # 각 종목별로 집계
                for stock in stocks:
                    if stock:
                        stock_data[stock]['total'] += 1
                        
                        if sentiment_score > 0:
                            stock_data[stock]['positive'] += 1
                        elif sentiment_score < 0:
                            stock_data[stock]['negative'] += 1
                        else:
                            stock_data[stock]['neutral'] += 1
                        
                        # 가중치 적용
                        stock_data[stock]['weighted_scores'].append(sentiment_score * time_weight)
                        stock_data[stock]['weights'].append(time_weight)
        
        # 결과 계산
        results = []
        for stock, data in stock_data.items():
            # 일반 감성 지수
            sentiment_index = self.calculate_sentiment_index(
                data['positive'], data['negative'], data['total']
            )
            
            # 가중 감성 지수
            if sum(data['weights']) > 0:
                weighted_sentiment_index = sum(data['weighted_scores']) / sum(data['weights'])
            else:
                weighted_sentiment_index = 0.0
            
            results.append({
                'stock': stock,
                'total': data['total'],
                'positive': data['positive'],
                'negative': data['negative'],
                'neutral': data['neutral'],
                'sentiment_index': sentiment_index,
                'weighted_sentiment_index': weighted_sentiment_index,
                'avg_weight': sum(data['weights']) / len(data['weights']) if data['weights'] else 0
            })
        
        return sorted(results, key=lambda x: x['weighted_sentiment_index'], reverse=True)
    
    @staticmethod
    def get_grade(sentiment_index: float) -> str:
        """
        감성 지수를 등급으로 변환
        
        Args:
            sentiment_index: 감성 지수 (-1.0 ~ +1.0)
            
        Returns:
            str: 등급
        """
        if sentiment_index > 0.5:
            return "매우 긍정적"
        elif sentiment_index > 0.2:
            return "긍정적"
        elif sentiment_index > -0.2:
            return "중립적"
        elif sentiment_index > -0.5:
            return "부정적"
        else:
            return "매우 부정적"
    
    def to_dataframe(self, results: List[Dict], add_grade: bool = True) -> pd.DataFrame:
        """
        결과를 DataFrame으로 변환
        
        Args:
            results: calculate 메서드의 반환값
            add_grade: 등급 컬럼 추가 여부
            
        Returns:
            pd.DataFrame: 결과 데이터프레임
        """
        df = pd.DataFrame(results)
        
        if add_grade and 'weighted_sentiment_index' in df.columns:
            df['등급'] = df['weighted_sentiment_index'].apply(self.get_grade)
        elif add_grade and 'sentiment_index' in df.columns:
            df['등급'] = df['sentiment_index'].apply(self.get_grade)
        
        return df
    
    def print_results(self, results: List[Dict], result_type: str = 'stock'):
        """
        결과를 표 형식으로 출력
        
        Args:
            results: calculate 메서드의 반환값
            result_type: 'stock' 또는 'keyword'
        """
        print("=" * 90)
        print(f"{'종목별' if result_type == 'stock' else '키워드별'} 감성 지수")
        print("=" * 90)
        
        name_key = 'stock' if result_type == 'stock' else 'keyword'
        
        for rank, r in enumerate(results, 1):
            emoji = "🟢" if r['sentiment_index'] > 0.3 else (
                "🔴" if r['sentiment_index'] < -0.3 else "🟡"
            )
            
            print(f"{rank}. {emoji} {r[name_key]:<20} | "
                  f"감성지수: {r['sentiment_index']:+.3f} | "
                  f"긍정: {r['positive']}  부정: {r['negative']}  전체: {r['total']}")


def calculate_final_recommendation_score(
    keyword_relevance: float,
    sentiment_index: float
) -> float:
    """
    최종 추천 점수 계산
    
    공식: (키워드 연관성 × 0.6) + (감성 지수 × 40 × 0.4)
    
    Args:
        keyword_relevance: 키워드 연관성 (0~10)
        sentiment_index: 감성 지수 (-1.0 ~ +1.0)
    
    Returns:
        float: 최종 추천 점수 (0~100)
    """
    keyword_score = keyword_relevance * 6.0
    sentiment_score = sentiment_index * 40
    return keyword_score + sentiment_score