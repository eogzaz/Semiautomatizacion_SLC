import streamlit as st
st.title("Documentación")
st.markdown("""
### Descripción del proyecto  

Se utilizan datos de observaciones de asteroides registradas en la base de datos del **MPC** y datos de efemérides generadas por el **JPL** para obtener la **magnitud absoluta** en distintos puntos de la órbita de los asteroides y con esto hacer la **curva de luz secular (SLC)** y la **curva de fase** de algún asteroide, todo esto con el objetivo de encontrar fluctuaciones que indiquen posible actividad cometaria.  

---

### Datos observacionales  
El **Minor Planet Center (MPC)**, entre sus variadas funciones, se encarga de recopilar información fotométrica de cada una de las observaciones realizadas sobre cuerpos menores del sistema solar, incluyendo asteroides. Esta base de datos puede ser consultada en el enlace: [MPC Explorer](https://data.minorplanetcenter.net/explorer/).  

Ahí encontrará una aplicación web intuitiva que permite buscar un objeto, determinar su identidad y recuperar información sobre su designación, efemérides, órbita y observaciones. En este explorador propio del MPC usan la última versión de la **API de Identificador de Designación**, la cual aún está en desarrollo. Antiguamente los datos estaban en otra base de datos del MPC y aún se pueden explorar en: [MPC DB Search](https://www.minorplanetcenter.net/db_search).  

En este notebook se usa la **API oficial para las observaciones del MPC**, la cual es un endpoint **REST** y, por lo tanto, se puede usar el lenguaje de programación que se prefiera. En este caso, se utiliza **Python** para enviar solicitudes `GET` a la URL:  
👉 `https://data.minorplanetcenter.net/api/get-obs`  

La función `observaciones_APIMPC` obtiene los datos observacionales de distintos objetos de la base del MPC utilizando la librería **requests**. Con solo conocer algún identificador del asteroide se obtienen los datos de la fecha, magnitud observada y filtro fotométrico utilizado en observación para todas las observaciones registradas de dicho asteroide.  

---

### Datos de efemérides  
Para obtener la **magnitud absoluta**, es decir, una magnitud con la cual se puedan comparar observaciones en distintos puntos de la órbita, es necesario obtener:  

- La **distancia del asteroide al Sol (r)**  
- La **distancia a la Tierra (Δ)**  
- El **ángulo de fase (α)**  

Estos datos se pueden obtener del sistema de efemérides del **JPL**, utilizando su API oficial **Horizons File API**.  

La función `efemerides_API` se conecta con la API del JPL y devuelve un DataFrame con las columnas:  
- Date  
- Date JD  
- Δ (distancia Tierra-asteroide)  
- r (distancia Sol-asteroide)  
- fase (ángulo de fase)  

---

### Período y fecha del perihelio  
Otros datos necesarios para obtener la curva de luz son el **período orbital** y la **fecha del perihelio**.  
Por el momento, se están obteniendo con **astroquery**.  

---

### Limpieza de datos  

#### Corrección a banda V  
En cada observación fotométrica se utiliza un filtro específico.  
La función `Correccion_Banda` selecciona solo las observaciones realizadas en el visible y, cuando es posible, transforma la magnitud medida en una banda específica a la **banda V**.  

👉 Más detalles en el documento: *Corrección a banda V observaciones MPC*.  

#### Día Juliano  
Para relacionar los datos de efemérides y los datos de observaciones se utiliza la fecha.  
Para simplificar este proceso, se hace en términos del **día juliano**.  

Además, para calcular la diferencia en días entre el perihelio y la fecha de observación se requiere esta conversión.  
Se definen las funciones:  
- `Date_to_julian`  
- `julian_to_date`  

---

### Diferencia t - T  
La función `Distancia_Perihelio` calcula la diferencia en días entre la fecha de la observación y la fecha del perihelio.  
Esta información es vital, pues se usa en el eje **x** de la **SLC**.  

---

### Obtención del DataFrame principal  
La función `obtencion_dataframe` es donde ocurre la magia ✨.  
Primero usa las funciones de obtención de datos, luego los limpia, y después hace un **join** entre los datos observacionales y las efemérides.  

Finalmente, calcula la magnitud absoluta de cada observación con la fórmula:  

$$
m(1,1,0) = m(\Delta, R, \\alpha) - 5 \\log(\Delta R) - \\beta \\alpha
$$
""")
