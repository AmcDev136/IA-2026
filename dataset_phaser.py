import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_graphviz
import graphviz
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar el dataset
file_path = r'D:\IA Verano 2026\Juego_Arbol\datos_arbol.csv'
dataset = pd.read_csv(file_path)

# Eliminar columnas innecesarias (como la vacía "Unnamed: 3")
#dataset = dataset.drop(columns=['Unnamed: 3'])

# Definir características (X) y etiquetas (y)
X = dataset.iloc[:, :2]  # Las dos primeras columnas son las características
y = dataset.iloc[:, 2]   # La tercera columna es la etiqueta

print(X)
# Dividir los datos en conjunto de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Crear el clasificador de Árbol de Decisión
clf = DecisionTreeClassifier()
# Entrenar el modelo
clf.fit(X_train, y_train)
y_predict = clf.predict(X_test)

print(X_test, y_predict)
# Exportar el árbol de decisión en formato DOT para su visualización

print("Accuracy:", accuracy_score(y_test, y_predict))
print("\nReporte de Clasificación:\n", classification_report(y_test, y_predict))

#cm = confusion_matrix(y_test, y_predict)
#sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
#            xticklabels=dataset.target_names,
#            yticklabels=dataset.target_names)
#plt.xlabel('Predicho')
#plt.ylabel('Real')
#plt.title('Matriz de Confusión')
#plt.show()

dot_data = export_graphviz(clf, out_file=None, 
                           feature_names=['Feature 1', 'Feature 2'],  
                           class_names=['Clase 0', 'Clase 1'],  
                           filled=True, rounded=True,  
                           special_characters=True)  

# Crear el gráfico con graphviz
graph = graphviz.Source(dot_data)

# Mostrar el gráfico
graph.view()