# Árbol AVL Interactivo

## 📋 Información del Proyecto
Implementación de un Árbol AVL con interfaz de línea de comandos que permite operaciones CRUD y visualización mediante Graphviz.

## 👥 Integrantes
| Nombre | Carnet | Participación |
|--------|---------|---------------|
| Nelson Ramirez | | 100% |

## 🚀 Características
- Inserción con balanceo automático
- Búsqueda eficiente O(log n)
- Eliminación con rebalanceo
- Carga masiva desde archivos CSV
- Visualización gráfica con Graphviz
- Interfaz CLI interactiva

## 📦 Requisitos
- Python 3.6+
- Graphviz instalado en el sistema
- Paquete `graphviz` de Python

## ⚡ Características Principales

### 📊 Operaciones Implementadas
| Operación | Descripción | Complejidad |
|-----------|-------------|-------------|
| **Inserción** | Agrega nuevos elementos manteniendo el balance AVL | O(log n) |
| **Búsqueda** | Localiza elementos en el árbol | O(log n) |
| **Eliminación** | Remueve elementos y rebalancea automáticamente | O(log n) |
| **Carga CSV** | Importa múltiples valores desde archivos CSV | O(m log n) |
| **Visualización** | Genera representación gráfica con Graphviz | O(n) |
| **Recorridos** | Implementa recorrido inorden para visualización ordenada | O(n) |

### 🔄 Tipos de Rotaciones
El árbol implementa las cuatro rotaciones fundamentales de AVL:

1. **Rotación Simple Derecha (LL)**
   - Caso: Factor de balance > 1 y el hijo izquierdo tiene balance ≥ 0
   - Escenario: Inserción en el subárbol izquierdo del hijo izquierdo

2. **Rotación Simple Izquierda (RR)**
   - Caso: Factor de balance < -1 y el hijo derecho tiene balance ≤ 0
   - Escenario: Inserción en el subárbol derecho del hijo derecho

3. **Rotación Doble Derecha (LR)**
   - Caso: Factor de balance > 1 y el hijo izquierdo tiene balance < 0
   - Secuencia: Rotación izquierda en hijo izquierdo + Rotación derecha en raíz

4. **Rotación Doble Izquierda (RL)**
   - Caso: Factor de balance < -1 y el hijo derecho tiene balance > 0
   - Secuencia: Rotación derecha en hijo derecho + Rotación izquierda en raíz

### 🎨 Visualización con Graphviz
- **Formato de salida:** PNG (Portable Network Graphics)
- **Información mostrada por nodo:**
  - Valor del nodo
  - Altura del nodo (h)
  - Factor de balance (b)
- **Características visuales:**
  - Nodos con forma circular
  - Color azul claro para mejor visibilidad
  - Conexiones jerárquicas claras
  - Distribución balanceada automática

---

## 📚 Fundamentos Teóricos

### Definición Formal de Árbol AVL
Un árbol binario de búsqueda T es un **Árbol AVL** si y solo si:
1. Es un árbol binario de búsqueda válido
2. Para cada nodo n en T: `|altura(n.izquierda) - altura(n.derecha)| ≤ 1`