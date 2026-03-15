# ============================================================
# IMDb Top 1000 Movies — Complete EDA Practice
# Date: March 15, 2026
# Author: Prajwal Kondala | IIT KGP -> Data Scientist
# Repo: python-practice
# Topics: Seaborn (full arsenal) + Plotly + Correlation +
#         Statistical Analysis + EDA Framework
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from scipy import stats

sns.set_style("whitegrid")
sns.set_palette("Set2")

# ============================================================
# STEP 1 — LOAD DATA
# ============================================================

df = pd.read_csv('imdb_top_1000.csv')
print("=" * 55)
print("STEP 1 — DATA OVERVIEW")
print("=" * 55)
print(f"Shape: {df.shape}")
print(f"\nColumns:\n{df.columns.tolist()}")
print(f"\nData Types:\n{df.dtypes}")
print(f"\nMissing Values:\n{df.isnull().sum()}")
print(f"\nBasic Stats:\n{df.describe()}")

# ============================================================
# STEP 2 — DATA CLEANING
# ============================================================

print("\n" + "=" * 55)
print("STEP 2 — DATA CLEANING")
print("=" * 55)

# Fix Released_Year dtype
df['Released_Year'] = pd.to_numeric(df['Released_Year'], errors='coerce')

# Fix Runtime — remove 'min' and convert to number
df['Runtime'] = df['Runtime'].str.replace(' min', '').astype(float)

# Fix Gross — remove commas and convert to number
df['Gross'] = df['Gross'].str.replace(',', '').astype(float)

# Handle missing values
# Meta_score → median (numerical, skewed like salary)
df['Meta_score'] = df['Meta_score'].fillna(df['Meta_score'].median())

# Certificate → Unknown (categorical)
df['Certificate'] = df['Certificate'].fillna('Unknown')

# Gross → median (heavily skewed, few blockbusters)
df['Gross'] = df['Gross'].fillna(df['Gross'].median())

# Released_Year → drop 1 row (can't guess a year!)
df = df.dropna(subset=['Released_Year'])
df['Released_Year'] = df['Released_Year'].astype(int)

# Feature Engineering
df['Primary_Genre'] = df['Genre'].str.split(',').str[0].str.strip()
df['Decade'] = (df['Released_Year'] // 10) * 10
df['gap'] = df['IMDB_Rating'] * 10 - df['Meta_score']

print(f"Final Shape: {df.shape}")
print(f"Missing Values after cleaning:\n{df.isnull().sum()}")
print("Cleaning Complete! ✅")

# ============================================================
# STEP 3 — UNIVARIATE ANALYSIS
# ============================================================

print("\n" + "=" * 55)
print("STEP 3 — UNIVARIATE ANALYSIS")
print("=" * 55)

# --- Chart 1: IMDB Rating Distribution ---
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

sns.histplot(df['IMDB_Rating'], bins=20,
             kde=True, ax=axes[0], color='steelblue')
axes[0].set_title('IMDB Rating Distribution')
axes[0].set_xlabel('Rating')

sns.boxplot(y=df['IMDB_Rating'], ax=axes[1])
axes[1].set_title('IMDB Rating Boxplot')

plt.tight_layout()
plt.savefig('01_imdb_rating_distribution.png', dpi=150)
plt.show()

print(f"\nIMDB Rating Stats:")
print(f"Mean   : {df['IMDB_Rating'].mean():.2f}")
print(f"Median : {df['IMDB_Rating'].median():.2f}")
print(f"Std    : {df['IMDB_Rating'].std():.2f}")
print(f"Skew   : {df['IMDB_Rating'].skew():.2f}")
print(f"\nTop rated movies (9.0+):")
print(df[df['IMDB_Rating'] >= 9.0][['Series_Title',
                                     'IMDB_Rating',
                                     'Released_Year',
                                     'Director']].sort_values('IMDB_Rating',
                                                               ascending=False))

# --- Chart 2: Runtime Distribution ---
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

sns.histplot(df['Runtime'], bins=30,
             kde=True, ax=axes[0], color='coral')
axes[0].set_title('Movie Runtime Distribution')
axes[0].set_xlabel('Runtime (minutes)')

sns.boxplot(y=df['Runtime'], ax=axes[1])
axes[1].set_title('Runtime Boxplot')

plt.tight_layout()
plt.savefig('02_runtime_distribution.png', dpi=150)
plt.show()

print(f"\nRuntime Stats:")
print(f"Mean   : {df['Runtime'].mean():.1f} mins")
print(f"Median : {df['Runtime'].median():.1f} mins")
print(f"Min    : {df['Runtime'].min():.0f} mins")
print(f"Max    : {df['Runtime'].max():.0f} mins")
print(f"\nLongest movies:")
print(df.nlargest(5, 'Runtime')[['Series_Title',
                                  'Runtime',
                                  'IMDB_Rating']])

# --- Chart 3: Gross Distribution ---
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

sns.histplot(df['Gross'], bins=30,
             kde=True, ax=axes[0], color='green')
axes[0].set_title('Gross Earnings Distribution')
axes[0].set_xlabel('Gross ($)')

sns.boxplot(y=df['Gross'], ax=axes[1])
axes[1].set_title('Gross Earnings Boxplot')

plt.tight_layout()
plt.savefig('03_gross_distribution.png', dpi=150)
plt.show()

print(f"\nGross Stats:")
print(f"Mean   : ${df['Gross'].mean():,.0f}")
print(f"Median : ${df['Gross'].median():,.0f}")
print(f"Max    : ${df['Gross'].max():,.0f}")
print(f"Skew   : {df['Gross'].skew():.2f}")
print(f"\nTop 5 highest grossing movies:")
print(df.nlargest(5, 'Gross')[['Series_Title',
                                'Released_Year',
                                'Gross',
                                'IMDB_Rating']])

# --- Categorical Overview ---
print(f"\nTop Genres:\n{df['Genre'].value_counts().head(10)}")
print(f"\nTop Certificates:\n{df['Certificate'].value_counts().head(8)}")
print(f"\nTop Directors:\n{df['Director'].value_counts().head(10)}")

# ============================================================
# STEP 4 — BIVARIATE ANALYSIS
# ============================================================

print("\n" + "=" * 55)
print("STEP 4 — BIVARIATE ANALYSIS")
print("=" * 55)

# --- Chart 4: Critics vs Audience ---
fig, ax = plt.subplots(figsize=(10, 6))

sns.scatterplot(data=df,
                x='Meta_score',
                y='IMDB_Rating',
                alpha=0.5,
                color='steelblue')

sns.regplot(data=df,
            x='Meta_score',
            y='IMDB_Rating',
            scatter=False,
            color='red',
            ax=ax)

correlation = df['Meta_score'].corr(df['IMDB_Rating'])
ax.set_title(f'Critics vs Audience Ratings\nr = {correlation:.2f}')
ax.set_xlabel('Meta Score (Critics)')
ax.set_ylabel('IMDB Rating (Audience)')

plt.savefig('04_critics_vs_audience.png', dpi=150)
plt.show()

print(f"\nCritics vs Audience Correlation: {correlation:.2f}")
print("Weak correlation — they fundamentally disagree!")

print(f"\nAudience loved, Critics didn't:")
print(df.nlargest(5, 'gap')[['Series_Title',
                              'IMDB_Rating',
                              'Meta_score',
                              'gap']])

print(f"\nCritics loved, Audience didn't:")
print(df.nsmallest(5, 'gap')[['Series_Title',
                               'IMDB_Rating',
                               'Meta_score',
                               'gap']])

# Interactive version with Plotly
fig = px.scatter(df,
                 x='Meta_score',
                 y='IMDB_Rating',
                 hover_name='Series_Title',
                 color='IMDB_Rating',
                 size='No_of_Votes',
                 title='Critics vs Audience — Hover to explore!',
                 labels={'Meta_score': 'Critics Score',
                         'IMDB_Rating': 'Audience Rating'})
fig.update_layout(template='plotly_white')
fig.show()

# --- Chart 5: Rating by Genre (Box Plot) ---
top_genres = df['Primary_Genre'].value_counts().head(8).index
df_genres = df[df['Primary_Genre'].isin(top_genres)]

plt.figure(figsize=(14, 6))
sns.boxplot(data=df_genres,
            x='Primary_Genre',
            y='IMDB_Rating',
            palette='Set2',
            hue='Primary_Genre',
            legend=False)

plt.title('IMDB Rating Distribution by Genre')
plt.xlabel('Genre')
plt.ylabel('IMDB Rating')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('05_rating_by_genre.png', dpi=150)
plt.show()

# Interactive Plotly version
fig = px.box(df_genres,
             x='Primary_Genre',
             y='IMDB_Rating',
             color='Primary_Genre',
             hover_name='Series_Title',
             title='IMDB Rating by Genre — Hover to see movies!',
             points='outliers')
fig.update_layout(template='plotly_white',
                  showlegend=False)
fig.show()

# --- Chart 6: Runtime by Genre (Violin Plot) ---
plt.figure(figsize=(14, 6))
sns.violinplot(data=df_genres,
               x='Primary_Genre',
               y='Runtime',
               palette='Set2',
               hue='Primary_Genre',
               legend=False)

plt.title('Movie Runtime Distribution by Genre')
plt.xlabel('Genre')
plt.ylabel('Runtime (minutes)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('06_runtime_by_genre.png', dpi=150)
plt.show()

# ============================================================
# STEP 5 — MULTIVARIATE ANALYSIS
# ============================================================

print("\n" + "=" * 55)
print("STEP 5 — MULTIVARIATE ANALYSIS")
print("=" * 55)

# --- Chart 7: Pairplot ---
numerical_cols = ['IMDB_Rating', 'Meta_score',
                  'Runtime', 'No_of_Votes', 'Gross']

sns.pairplot(df[numerical_cols],
             diag_kind='kde',
             plot_kws={'alpha': 0.5})

plt.suptitle('Pairplot — All Numerical Relationships',
             y=1.02, fontsize=14)
plt.savefig('07_pairplot.png', dpi=150, bbox_inches='tight')
plt.show()

# --- Chart 8: Correlation Heatmap ---
plt.figure(figsize=(10, 8))

corr_matrix = df[numerical_cols].corr()
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))

sns.heatmap(corr_matrix,
            annot=True,
            fmt='.2f',
            cmap='coolwarm',
            mask=mask,
            vmin=-1, vmax=1,
            square=True,
            linewidths=0.5)

plt.title('Correlation Heatmap — IMDb Top 1000')
plt.tight_layout()
plt.savefig('08_correlation_heatmap.png', dpi=150)
plt.show()

print("\nCorrelation Summary:")
print(f"IMDB_Rating vs No_of_Votes : {df['IMDB_Rating'].corr(df['No_of_Votes']):.2f}")
print(f"IMDB_Rating vs Gross       : {df['IMDB_Rating'].corr(df['Gross']):.2f}")
print(f"No_of_Votes vs Gross       : {df['No_of_Votes'].corr(df['Gross']):.2f}")
print(f"Meta_score vs IMDB_Rating  : {df['Meta_score'].corr(df['IMDB_Rating']):.2f}")
print(f"Runtime vs Meta_score      : {df['Runtime'].corr(df['Meta_score']):.2f}")

# ============================================================
# STEP 6 — DEEPER INSIGHTS WITH PLOTLY
# ============================================================

print("\n" + "=" * 55)
print("STEP 6 — DEEPER INSIGHTS")
print("=" * 55)

# --- Chart 9: Top Directors by Movie Count ---
top_directors = df['Director'].value_counts().head(10).reset_index()
top_directors.columns = ['Director', 'Movie_Count']

fig = px.bar(top_directors,
             x='Movie_Count',
             y='Director',
             orientation='h',
             color='Movie_Count',
             title='Top 10 Directors by Number of Movies',
             text='Movie_Count')

fig.update_layout(template='plotly_white',
                  yaxis={'categoryorder': 'total ascending'},
                  coloraxis_showscale=False)
fig.show()

# --- Chart 10: Top Directors by Average Rating ---
top_dir_rating = df.groupby('Director')['IMDB_Rating'].agg(
    ['mean', 'count']).reset_index()

top_dir_rating = top_dir_rating[top_dir_rating['count'] >= 3]
top_dir_rating = top_dir_rating.nlargest(10, 'mean')
top_dir_rating.columns = ['Director', 'Avg_Rating', 'Movie_Count']

fig = px.bar(top_dir_rating,
             x='Avg_Rating',
             y='Director',
             orientation='h',
             color='Avg_Rating',
             title='Top Directors by Average Rating (min 3 movies)',
             text='Avg_Rating',
             hover_data=['Movie_Count'])

fig.update_traces(texttemplate='%{text:.2f}')
fig.update_layout(template='plotly_white',
                  yaxis={'categoryorder': 'total ascending'},
                  coloraxis_showscale=False)
fig.show()

print("\nTop director by consistency (3+ movies):")
print(top_dir_rating.head(3)[['Director',
                               'Avg_Rating',
                               'Movie_Count']])

# --- Chart 11: Movies by Decade ---
decade_stats = df.groupby('Decade').agg(
    Avg_Rating=('IMDB_Rating', 'mean'),
    Movie_Count=('IMDB_Rating', 'count'),
    Avg_Gross=('Gross', 'mean')
).reset_index()

fig = px.line(decade_stats,
              x='Decade',
              y='Avg_Rating',
              markers=True,
              title='Average IMDB Rating by Decade',
              text='Movie_Count')

fig.update_traces(textposition='top center')
fig.update_layout(template='plotly_white',
                  xaxis_title='Decade',
                  yaxis_title='Average Rating',
                  yaxis=dict(range=[7.5, 9.0]))
fig.show()

print(f"\nMovies per decade:")
print(decade_stats[['Decade',
                     'Movie_Count',
                     'Avg_Rating']].to_string(index=False))

# --- Chart 12: Top Grossing Movies ---
top_gross = df.nlargest(15, 'Gross')

fig = px.bar(top_gross,
             x='Gross',
             y='Series_Title',
             orientation='h',
             color='IMDB_Rating',
             title='Top 15 Highest Grossing Movies',
             hover_data=['Released_Year',
                        'IMDB_Rating',
                        'Primary_Genre'],
             text='IMDB_Rating')

fig.update_traces(texttemplate='%{text:.1f}⭐')
fig.update_layout(template='plotly_white',
                  yaxis={'categoryorder': 'total ascending'},
                  coloraxis_colorbar_title='Rating',
                  xaxis_title='Gross Earnings ($)')
fig.show()

# ============================================================
# STEP 7 — KEY INSIGHTS SUMMARY
# ============================================================

print("\n" + "=" * 55)
print("KEY INSIGHTS — IMDb Top 1000 EDA")
print("=" * 55)

print(f"\n1. Rating range: {df['IMDB_Rating'].min()} "
      f"to {df['IMDB_Rating'].max()}")
print(f"   Only 5 movies rated 9.0+ — true legends!")

print(f"\n2. Average runtime: {df['Runtime'].mean():.0f} mins")
print(f"   Longest: Gangs of Wasseypur at "
      f"{df['Runtime'].max():.0f} mins!")

print(f"\n3. Critics vs Audience correlation: 0.26")
print(f"   Weak! They fundamentally disagree!")

print(f"\n4. Quality vs Money correlation: 0.09")
print(f"   Almost zero! Great movies don't always earn!")

print(f"\n5. Popularity vs Money correlation: 0.59")
print(f"   Strongest! Popularity drives earnings!")

print(f"\n6. Top genre by rating: Crime")
print(f"   Carried by Godfather, 12 Angry Men, Pulp Fiction!")

print(f"\n7. Best director consistency: Christopher Nolan")
print(f"   Most movies in top 1000: Alfred Hitchcock")

print(f"\n8. Best decade: 2010s — 242 movies!")
print(f"   Streaming era improved quality!")

print(f"\n9. Highest grossing: Star Wars Ep7 — $936M")
print(f"   But rated only 7.9 — money != quality!")

print("\n" + "=" * 55)
print("EDA COMPLETE! Charts saved in screenshots/")
print("=" * 55)
