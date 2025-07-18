#!/usr/bin/env python
# coding: utf-8

# In[5]:


import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

def load_json_data():
    try:
        with open('user-wallet-transactions.json') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: user-wallet-transactions.json not found in current directory")
        exit(1)
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in user-wallet-transactions.json")
        exit(1)

def generate_analysis_report(scores, details):
    bins = [0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
    labels = ['0-100', '100-200', '200-300', '300-400', '400-500', 
              '500-600', '600-700', '700-800', '800-900', '900-1000']
    
    score_values = list(scores.values())
    hist, _ = np.histogram(score_values, bins=bins)
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(labels, hist, color=['#ff6b6b', '#ffa502', '#feca57', '#ff9ff3', 
                                      '#48dbfb', '#1dd1a1', '#00d2d3', '#5f27cd', 
                                      '#341f97', '#01a3a4'])
    plt.xlabel('Credit Score Range', fontsize=12)
    plt.ylabel('Number of Wallets', fontsize=12)
    plt.title('Aave V2 Wallet Credit Score Distribution', fontsize=14, pad=20)
    
    for bar in bars:
        height = bar.get_height()
        if height > 0:
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}', ha='center', va='bottom')
    
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('aave_credit_score_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    df = pd.DataFrame.from_dict(details, orient='index')
    
    categories = [
        ('Very Poor', 0, 200),
        ('Poor', 200, 400),
        ('Fair', 400, 600),
        ('Good', 600, 800),
        ('Excellent', 800, 1000)
    ]
    
    with open('aave_wallet_credit_analysis.md', 'w', encoding='utf-8') as f:
        f.write("# Aave V2 Wallet Credit Score Analysis\n\n")
        f.write("## Overview\n\n")
        f.write(f"Analyzed {len(scores)} unique wallets from user-wallet-transactions.json\n\n")
        f.write("![Credit Score Distribution](aave_credit_score_distribution.png)\n\n")
        
        f.write("## Score Distribution\n")
        f.write("| Score Range | Number of Wallets | Percentage |\n")
        f.write("|-------------|-------------------|------------|\n")
        for label, count in zip(labels, hist):
            percentage = (count / len(scores)) * 100
            f.write(f"| {label} | {count} | {percentage:.1f}% |\n")
        
        f.write("\n## Detailed Wallet Analysis by Credit Category\n")
        
        for name, lower, upper in categories:
            cat_df = df[(df['score'] >= lower) & (df['score'] < upper)]
            if len(cat_df) == 0:
                continue
                
            f.write(f"\n### {name} ({lower}-{upper})\n")
            f.write(f"Count: {len(cat_df)} wallets ({len(cat_df)/len(df)*100:.1f}% of total)\n\n")
            
            f.write("Behavioral Characteristics:\n")
            f.write(f"- 📊 Transactions: Median {cat_df['tx_count'].median():.1f} per wallet\n")
            f.write(f"- 🏦 Assets: Median {cat_df['assets'].apply(len).median():.1f} different assets\n")
            f.write(f"- 💰 Deposit Ratio: Median {cat_df['deposit_ratio'].median():.1%}\n")
            f.write(f"- ⚠️ Liquidations: {cat_df['liquidations'].gt(0).mean()*100:.1f}% of wallets\n")
            f.write(f"- 🕒 Wallet Age: Median {cat_df['wallet_age_days'].median():.1f} days\n")
            f.write(f"- 🤖 Bot-like Patterns: {cat_df['bot_like'].mean()*100:.1f}% of wallets\n")
            f.write(f"- 💵 Median Volume: ${cat_df['total_usd_volume'].median():,.2f} USD\n\n")
        
        f.write("\n## Risk Recommendations\n\n")
        f.write("| Category | Suggested Action |\n")
        f.write("|----------|------------------|\n")
        f.write("| Excellent (800-1000) | Offer preferential rates, higher limits |\n")
        f.write("| Good (600-800) | Monitor for upgrade potential |\n")
        f.write("| Fair (400-600) | Educational outreach, moderate limits |\n")
        f.write("| Poor (200-400) | Reduced limits, increased monitoring |\n")
        f.write("| Very Poor (0-200) | Strict limits, potential restrictions |\n")
        
        f.write("\n## Methodology\n\n")
        f.write("Credit scores (0-1000) incorporate:\n")
        f.write("- Transaction Activity (25%): Frequency and consistency\n")
        f.write("- Asset Diversity (20%): Variety of assets interacted with\n")
        f.write("- Deposit Behavior (35%): Deposit-to-borrow ratio\n")
        f.write("- Wallet Longevity (20%): Account age and activity duration\n")
        f.write("- Risk Penalties: Liquidations (-100 each), bot-like patterns (-150), value volatility\n")

def main():
    print("Loading data from user-wallet-transactions.json...")
    data = load_json_data()
    
    print(f"Calculating credit scores for {len(data)} transactions...")
    scores, details = calculate_credit_scores(data)
    
    print("Generating analysis report...")
    generate_analysis_report(scores, details)
    
    print("\n✅ Analysis complete!")
    print(f"- Processed {len(scores)} unique wallets")
    print("- Saved report to 'aave_wallet_credit_analysis.md'")
    print("- Saved visualization to 'aave_credit_score_distribution.png'")

if __name__ == "__main__":
    main()

