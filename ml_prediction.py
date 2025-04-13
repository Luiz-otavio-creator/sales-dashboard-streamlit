# Importação de bibliotecas
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import warnings
warnings.filterwarnings('ignore')

# Bibliotecas de Machine Learning
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import joblib

# Carregando os dados
df = pd.read_csv('data/sales_data.csv')  # Caminho correto do seu CSV

# Visualizar as primeiras linhas
print('Colunas disponíveis:', df.columns.tolist())
print(df.head())

# Convertendo datas e extraindo o mês
df['Date'] = pd.to_datetime(df['Date'])
df['Month'] = df['Date'].dt.month

# Corrigir o nome da função: get_dummies (estava errado)
df = pd.get_dummies(df, columns=["Product", "Category", "Region", "Seller"], drop_first=True)

# Selecionar X e y
X = df.drop(['Total', 'Date'], axis=1)  # axis=1 (não axis_1)
y = df['Total']

# Dividir os dados
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Treinar modelo
model = LinearRegression()
model.fit(X_train, y_train)

# Prever
y_pred = model.predict(X_test)

# Avaliação
print("MAE:", mean_absolute_error(y_test, y_pred))
print("MSE:", mean_squared_error(y_test, y_pred))
print("R²:", r2_score(y_test, y_pred))

# Comparação
resultado = pd.DataFrame({"Valor Real": y_test, "Previsto": y_pred})
st.subheader("🔍 Comparação: Real vs. Previsto")
st.dataframe(resultado.head(10))

# Gráfico de dispersão
st.subheader("📈 Gráfico: Valor Real vs. Valor Previsto")
fig, ax = plt.subplots()
sns.scatterplot(x=y_test, y=y_pred, ax=ax)
ax.set_xlabel("Valor Real")
ax.set_ylabel("Valor Previsto")
ax.set_title("Dispersão dos Valores Reais vs. Previstos")
st.pyplot(fig)

# Salvar modelo
joblib.dump(model, 'modelos/modelo_vendas.pkl')  # Corrigido o caminho para a pasta "modelos"
