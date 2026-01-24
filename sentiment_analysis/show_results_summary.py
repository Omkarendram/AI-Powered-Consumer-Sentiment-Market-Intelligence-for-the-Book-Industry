import pandas as pd

df = pd.read_csv(r'c:\Users\KIIT0001\Downloads\infosys\infosys\ai-consumer-sentiment-data-collection\data\processed\sentiment_analysis_results.csv')

print('='*60)
print('SENTIMENT ANALYSIS RESULTS SUMMARY')
print('='*60)
print(f'\nTotal Records Analyzed: {len(df)}')

print('\n--- SENTIMENT DISTRIBUTION ---')
sentiment_counts = df['sentiment'].value_counts()
for sentiment in ['positive', 'negative', 'neutral']:
    if sentiment in sentiment_counts.index:
        count = sentiment_counts[sentiment]
        percentage = (count / len(df)) * 100
        print(f'  {sentiment.upper():10} : {count:3d} ({percentage:6.2f}%)')

print('\n--- CONFIDENCE SCORES ---')
print(f'  Mean     : {df["confidence"].mean():.2f}')
print(f'  Median   : {df["confidence"].median():.2f}')
print(f'  Min      : {df["confidence"].min():.2f}')
print(f'  Max      : {df["confidence"].max():.2f}')
print(f'  Std Dev  : {df["confidence"].std():.2f}')

print('\n--- CONFIDENCE BY SENTIMENT ---')
for sentiment in ['positive', 'negative', 'neutral']:
    subset = df[df['sentiment'] == sentiment]['confidence']
    if len(subset) > 0:
        print(f'  {sentiment.upper():10} : Mean={subset.mean():.2f}, Median={subset.median():.2f}')

print('\n' + '='*60)
print('Results file:')
print('c:\\Users\\KIIT0001\\Downloads\\infosys\\infosys\\ai-consumer-sentiment-data-collection\\data\\processed\\sentiment_analysis_results.csv')
print('='*60)
