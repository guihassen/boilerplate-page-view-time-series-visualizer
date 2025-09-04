import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'])
df = df.set_index("date")

# Clean data
# limpando o df para ficar somente com a 2.5% acima e 2.5% abaixo
df = df[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]


def draw_line_plot():
    # Draw line plot
    #criando a figura para colocar os gráficos
    fig, ax = plt.subplots(figsize=(15, 5))
    #desenhando a linha vermelha que conecta os dados
    ax.plot(df.index, df['value'], color='r', linewidth=1)
    ax.set_title('Daily Views from 5/2016 to 12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig


def draw_bar_plot():
    #copiando o df para não alterar o principal
    df_bar = df.copy()
    #adicionando as colunas de mês e ano
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month
    
    #agrupando os valores por mês e ano e após isso transformando anos em linhas e meses em colunas
    grouped_month = df_bar.groupby(['year', 'month'])['value'].mean().unstack().round()
    
    #criando o gráfico
    fig, ax = plt.subplots()
    fig = grouped_month.plot.bar(figsize=(10, 8)).figure
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    plt.legend(title='Months')

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig


# Draw box plots (using Seaborn)    
def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    
    # Garantir que a coluna date é datetime
    df_box['date'] = pd.to_datetime(df_box['date'])
    
    # Extrair ano e mês de forma segura
    df_box['year'] = df_box['date'].dt.year
    df_box['month'] = df_box['date'].dt.strftime('%b')
    
    # Remover valores nulos se houver
    df_box = df_box.dropna(subset=['year', 'month', 'value'])
    
    print(f"Dados após limpeza: {len(df_box)} linhas")
    print(f"Meses únicos: {sorted(df_box['month'].unique())}")
    print(f"Anos únicos: {sorted(df_box['year'].unique())}")

    # Draw box plots (using Seaborn)
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))

    # Year-wise Box Plot (Trend)
    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')

    # Month-wise Box Plot (Seasonality)
    sns.boxplot(x='month', y='value', data=df_box, ax=axes[1])
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig



