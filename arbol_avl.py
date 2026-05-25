import csv
import os
from typing import Optional, Any, List


class Nodo:
    """Clase que representa un nodo en el árbol binario"""
    
    def __init__(self, valor: Any):
        self.valor = valor
        self.izquierda: Optional[Nodo] = None
        self.derecha: Optional[Nodo] = None
        self.altura: int = 1


class ArbolBinarioBusqueda:
    """Clase base para Árbol Binario de Búsqueda"""
    
    def __init__(self):
        self.raiz: Optional[Nodo] = None
    
    def insertar(self, valor: Any) -> None:
        """Inserta un valor en el árbol"""
        self.raiz = self._insertar_recursivo(self.raiz, valor)
    
    def _insertar_recursivo(self, nodo: Optional[Nodo], valor: Any) -> Nodo:
        """Inserción recursiva en ABB"""
        if nodo is None:
            return Nodo(valor)
        
        if valor < nodo.valor:
            nodo.izquierda = self._insertar_recursivo(nodo.izquierda, valor)
        elif valor > nodo.valor:
            nodo.derecha = self._insertar_recursivo(nodo.derecha, valor)
        
        return nodo
    
    def buscar(self, valor: Any) -> bool:
        """Busca un valor en el árbol"""
        return self._buscar_recursivo(self.raiz, valor)
    
    def _buscar_recursivo(self, nodo: Optional[Nodo], valor: Any) -> bool:
        """Búsqueda recursiva en ABB"""
        if nodo is None:
            return False
        
        if valor == nodo.valor:
            return True
        elif valor < nodo.valor:
            return self._buscar_recursivo(nodo.izquierda, valor)
        else:
            return self._buscar_recursivo(nodo.derecha, valor)
    
    def eliminar(self, valor: Any) -> None:
        """Elimina un valor del árbol"""
        self.raiz = self._eliminar_recursivo(self.raiz, valor)
    
    def _eliminar_recursivo(self, nodo: Optional[Nodo], valor: Any) -> Optional[Nodo]:
        """Eliminación recursiva en ABB"""
        if nodo is None:
            return None
        
        if valor < nodo.valor:
            nodo.izquierda = self._eliminar_recursivo(nodo.izquierda, valor)
        elif valor > nodo.valor:
            nodo.derecha = self._eliminar_recursivo(nodo.derecha, valor)
        else:
            # Nodo con un solo hijo o sin hijos
            if nodo.izquierda is None:
                return nodo.derecha
            elif nodo.derecha is None:
                return nodo.izquierda
            
            # Nodo con dos hijos
            sucesor = self._encontrar_minimo(nodo.derecha)
            nodo.valor = sucesor.valor
            nodo.derecha = self._eliminar_recursivo(nodo.derecha, sucesor.valor)
        
        return nodo
    
    def _encontrar_minimo(self, nodo: Nodo) -> Nodo:
        """Encuentra el nodo con el valor mínimo"""
        actual = nodo
        while actual.izquierda is not None:
            actual = actual.izquierda
        return actual
    
    def recorrido_inorden(self) -> List[Any]:
        """Retorna el recorrido inorden del árbol"""
        resultado = []
        self._recorrido_inorden_recursivo(self.raiz, resultado)
        return resultado
    
    def _recorrido_inorden_recursivo(self, nodo: Optional[Nodo], resultado: List[Any]) -> None:
        """Recorrido inorden recursivo"""
        if nodo:
            self._recorrido_inorden_recursivo(nodo.izquierda, resultado)
            resultado.append(nodo.valor)
            self._recorrido_inorden_recursivo(nodo.derecha, resultado)


class ArbolAVL(ArbolBinarioBusqueda):
    """Clase para Árbol AVL que extiende de ABB"""
    
    def _obtener_altura(self, nodo: Optional[Nodo]) -> int:
        """Obtiene la altura de un nodo"""
        if nodo is None:
            return 0
        return nodo.altura
    
    def _actualizar_altura(self, nodo: Nodo) -> None:
        """Actualiza la altura de un nodo"""
        nodo.altura = 1 + max(self._obtener_altura(nodo.izquierda), 
                             self._obtener_altura(nodo.derecha))
    
    def _obtener_balance(self, nodo: Optional[Nodo]) -> int:
        """Calcula el factor de balance de un nodo"""
        if nodo is None:
            return 0
        return self._obtener_altura(nodo.izquierda) - self._obtener_altura(nodo.derecha)
    
    def _rotacion_derecha(self, y: Nodo) -> Nodo:
        """Realiza una rotación simple a la derecha"""
        x = y.izquierda
        T2 = x.derecha
        
        # Rotación
        x.derecha = y
        y.izquierda = T2
        
        # Actualizar alturas
        self._actualizar_altura(y)
        self._actualizar_altura(x)
        
        return x
    
    def _rotacion_izquierda(self, x: Nodo) -> Nodo:
        """Realiza una rotación simple a la izquierda"""
        y = x.derecha
        T2 = y.izquierda
        
        # Rotación
        y.izquierda = x
        x.derecha = T2
        
        # Actualizar alturas
        self._actualizar_altura(x)
        self._actualizar_altura(y)
        
        return y
    
    def _balancear(self, nodo: Nodo, valor: Any = None) -> Nodo:
        """Balancea el árbol después de inserción o eliminación"""
        # Actualizar altura
        self._actualizar_altura(nodo)
        
        # Obtener factor de balance
        balance = self._obtener_balance(nodo)
        
        # Casos de desbalance
        
        # Caso Izquierda-Izquierda
        if balance > 1 and self._obtener_balance(nodo.izquierda) >= 0:
            return self._rotacion_derecha(nodo)
        
        # Caso Derecha-Derecha
        if balance < -1 and self._obtener_balance(nodo.derecha) <= 0:
            return self._rotacion_izquierda(nodo)
        
        # Caso Izquierda-Derecha
        if balance > 1 and self._obtener_balance(nodo.izquierda) < 0:
            nodo.izquierda = self._rotacion_izquierda(nodo.izquierda)
            return self._rotacion_derecha(nodo)
        
        # Caso Derecha-Izquierda
        if balance < -1 and self._obtener_balance(nodo.derecha) > 0:
            nodo.derecha = self._rotacion_derecha(nodo.derecha)
            return self._rotacion_izquierda(nodo)
        
        return nodo
    
    def _insertar_recursivo(self, nodo: Optional[Nodo], valor: Any) -> Nodo:
        """Inserción recursiva con balanceo AVL"""
        # Inserción ABB
        if nodo is None:
            return Nodo(valor)
        
        if valor < nodo.valor:
            nodo.izquierda = self._insertar_recursivo(nodo.izquierda, valor)
        elif valor > nodo.valor:
            nodo.derecha = self._insertar_recursivo(nodo.derecha, valor)
        else:
            return nodo  # No se permiten duplicados
        
        # Balancear
        return self._balancear(nodo, valor)
    
    def _eliminar_recursivo(self, nodo: Optional[Nodo], valor: Any) -> Optional[Nodo]:
        """Eliminación recursiva con balanceo AVL"""
        # Eliminación ABB
        if nodo is None:
            return None
        
        if valor < nodo.valor:
            nodo.izquierda = self._eliminar_recursivo(nodo.izquierda, valor)
        elif valor > nodo.valor:
            nodo.derecha = self._eliminar_recursivo(nodo.derecha, valor)
        else:
            # Nodo con un solo hijo o sin hijos
            if nodo.izquierda is None:
                return nodo.derecha
            elif nodo.derecha is None:
                return nodo.izquierda
            
            # Nodo con dos hijos
            sucesor = self._encontrar_minimo(nodo.derecha)
            nodo.valor = sucesor.valor
            nodo.derecha = self._eliminar_recursivo(nodo.derecha, sucesor.valor)
        
        if nodo is None:
            return None
        
        # Balancear
        return self._balancear(nodo)
    
    def cargar_desde_csv(self, archivo: str) -> bool:
        """Carga valores desde un archivo CSV"""
        try:
            with open(archivo, 'r') as file:
                lector = csv.reader(file)
                for fila in lector:
                    for valor in fila:
                        try:
                            num = int(valor.strip())
                            self.insertar(num)
                        except ValueError:
                            print(f"Advertencia: '{valor}' no es un número válido, ignorado.")
            return True
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo '{archivo}'")
            return False
        except Exception as e:
            print(f"Error al leer el archivo: {e}")
            return False
    
    def generar_graphviz(self, nombre_archivo: str = "arbol_avl") -> None:
        """Genera una representación visual del árbol usando Graphviz"""
        dot_content = self._generar_dot()
        
        # Guardar archivo .dot
        with open(f"{nombre_archivo}.dot", "w") as file:
            file.write(dot_content)
        
        # Generar imagen
        os.system(f"dot -Tpng {nombre_archivo}.dot -o {nombre_archivo}.png")
        print(f"Árbol visualizado en {nombre_archivo}.png")
    
    def _generar_dot(self) -> str:
        """Genera el contenido DOT para Graphviz"""
        dot = ["digraph AVL {"]
        dot.append("    node [shape=circle, fontcolor=black, style=filled, fillcolor=lightblue];")
        dot.append("    rankdir=TB;")
        
        if self.raiz:
            self._generar_dot_recursivo(self.raiz, dot)
        
        dot.append("}")
        return "\n".join(dot)
    
    def _generar_dot_recursivo(self, nodo: Optional[Nodo], dot: List[str], padre: Optional[str] = None) -> None:
        """Genera recursivamente el contenido DOT"""
        if nodo is None:
            return
        
        node_id = str(id(nodo))
        balance = self._obtener_balance(nodo)
        label = f"{nodo.valor}\\n(h={nodo.altura}, b={balance})"
        dot.append(f'    "{node_id}" [label="{label}"];')
        
        if padre:
            dot.append(f'    "{padre}" -> "{node_id}";')
        
        self._generar_dot_recursivo(nodo.izquierda, dot, node_id)
        self._generar_dot_recursivo(nodo.derecha, dot, node_id)


class InterfazAVL:
    """Clase para la interfaz de línea de comandos"""
    
    def __init__(self):
        self.arbol = ArbolAVL()
    
    def mostrar_menu(self) -> None:
        """Muestra el menú principal"""
        print("\n" + "="*50)
        print("           ÁRBOL AVL INTERACTIVO")
        print("="*50)
        print("1. Insertar un número")
        print("2. Buscar un número")
        print("3. Eliminar un número")
        print("4. Cargar árbol desde archivo CSV")
        print("5. Visualizar árbol (Graphviz)")
        print("6. Mostrar recorrido inorden")
        print("7. Salir")
        print("="*50)
    
    def ejecutar(self) -> None:
        """Ejecuta el programa principal"""
        while True:
            self.mostrar_menu()
            opcion = input("\nSeleccione una opción (1-7): ").strip()
            
            if opcion == "1":
                self._insertar_numero()
            elif opcion == "2":
                self._buscar_numero()
            elif opcion == "3":
                self._eliminar_numero()
            elif opcion == "4":
                self._cargar_csv()
            elif opcion == "5":
                self._visualizar_arbol()
            elif opcion == "6":
                self._mostrar_inorden()
            elif opcion == "7":
                print("\n¡Gracias por usar el programa!")
                break
            else:
                print("\nOpción inválida. Por favor, seleccione 1-7.")
    
    def _insertar_numero(self) -> None:
        """Maneja la inserción de un número"""
        try:
            valor = int(input("\nIngrese el número a insertar: "))
            self.arbol.insertar(valor)
            print(f"✓ Número {valor} insertado correctamente.")
        except ValueError:
            print("✗ Error: Debe ingresar un número válido.")
    
    def _buscar_numero(self) -> None:
        """Maneja la búsqueda de un número"""
        try:
            valor = int(input("\nIngrese el número a buscar: "))
            if self.arbol.buscar(valor):
                print(f"✓ El número {valor} SÍ está en el árbol.")
            else:
                print(f"✗ El número {valor} NO está en el árbol.")
        except ValueError:
            print("✗ Error: Debe ingresar un número válido.")
    
    def _eliminar_numero(self) -> None:
        """Maneja la eliminación de un número"""
        try:
            valor = int(input("\nIngrese el número a eliminar: "))
            if self.arbol.buscar(valor):
                self.arbol.eliminar(valor)
                print(f"✓ Número {valor} eliminado correctamente.")
            else:
                print(f"✗ El número {valor} no existe en el árbol.")
        except ValueError:
            print("✗ Error: Debe ingresar un número válido.")
    
    def _cargar_csv(self) -> None:
        """Maneja la carga desde archivo CSV"""
        archivo = input("\nIngrese el nombre del archivo CSV: ").strip()
        if self.arbol.cargar_desde_csv(archivo):
            print(f"✓ Datos cargados correctamente desde '{archivo}'.")
    
    def _visualizar_arbol(self) -> None:
        """Maneja la visualización del árbol"""
        if self.arbol.raiz is None:
            print("\n✗ El árbol está vacío. No hay nada que visualizar.")
            return
        
        nombre = input("\nIngrese nombre para la imagen (Enter para 'arbol_avl'): ").strip()
        if not nombre:
            nombre = "arbol_avl"
        
        print("\nGenerando visualización...")
        self.arbol.generar_graphviz(nombre)
    
    def _mostrar_inorden(self) -> None:
        """Muestra el recorrido inorden del árbol"""
        if self.arbol.raiz is None:
            print("\n✗ El árbol está vacío.")
            return
        
        recorrido = self.arbol.recorrido_inorden()
        print(f"\nRecorrido inorden: {recorrido}")


def main():
    """Función principal"""
    interfaz = InterfazAVL()
    interfaz.ejecutar()


if __name__ == "__main__":
    main()