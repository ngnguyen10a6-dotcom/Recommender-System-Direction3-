# -*- coding: utf-8 -*-
"""Direction3_Popularity_Bias.py
Thực hiện Hướng 3: Popularity Bias Mitigation & Reranking
"""
import pandas as pd
import numpy as np
import os

def run():
    print("Executing Direction 3 Popularity Bias Mitigation...")
    df_catalog = pd.read_excel('All_Beauty_Cleaned_Merged_GitHub.xlsx')
    df_candidates = pd.read_csv('kg_llm_recommendations_for_member3.csv')
    
    pop_dict = dict(zip(df_catalog['parent_asin'], df_catalog['rating_count']))
    df_candidates['popularity'] = df_candidates['recommended_items'].map(pop_dict).fillna(0)
    
    pop_values = list(pop_dict.values())
    head_thresh = np.percentile(pop_values, 80)
    tail_thresh = np.percentile(pop_values, 20)
    
    def get_group(pop):
        return 'Head' if pop >= head_thresh else ('Tail' if pop <= tail_thresh else 'Mid')
        
    df_candidates['group'] = df_candidates['popularity'].apply(get_group)
    df_candidates['tail_bonus'] = 1.0 / np.log(1.0 + df_candidates['popularity'] + 1e-5)
    
    rel_min, rel_max = df_candidates['score'].min(), df_candidates['score'].max()
    bonus_min, bonus_max = df_candidates['tail_bonus'].min(), df_candidates['tail_bonus'].max()
    
    df_candidates['norm_rel'] = (df_candidates['score'] - rel_min) / (rel_max - rel_min + 1e-8)
    df_candidates['norm_bonus'] = (df_candidates['tail_bonus'] - bonus_min) / (bonus_max - bonus_min + 1e-8)
    
    # Selected Lambda = 0.3
    df_candidates['new_score'] = df_candidates['norm_rel'] + 0.3 * df_candidates['norm_bonus']
    final_top10 = df_candidates.sort_values(['user_id', 'new_score'], ascending=[True, False]).groupby('user_id').head(10)
    
    final_top10.to_csv('reranked_top10_direction3.csv', index=False)
    print("Done! Saved to reranked_top10_direction3.csv")

if __name__ == '__main__':
    run()
