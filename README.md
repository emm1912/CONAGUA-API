# CONAGUA-API
Utilizando la API de Conagua

Utilizando API de conagua para obtener la informacion del clima, se selecciona el estado y municipio y al finalizar manda un correo con la información del clima a una cuenta de correo selecionada.
Puede modificarse y servir como base para automatizar una casa si se esta monitoreando el clima.

Se deben configurar estas variables para que el programa tenga acceso a una cuenta de correo y su contraseña, que es desde donde manda el correo de respuesta (en mi caso utilice una cuenta de gmail).

<code>
EMAIL_ADDRESS = os.environ.get("GOOGLE_USER")
EMAIL_PASSWORD = os.environ.get("GOOGLE_PASS")
</code>

Aqui se escribe la direccion de correo a la que se quiere mandar la info del clima
<code>
email("\<AQUI ESCRIBE TU CORREO\>", "Clima", f"{  datosMeteorologicos(e,m, d,r_json)  } ")
</code>
Basicamente lo que hace el programa es bajar el archivo comprimido que entrega la API de conagua la descomprime y carga los valores en la variable "r_json". Despues pasamos por las preguntas para identificar estado y municipio, para finalmente por medio del metodo "datosMeteorologicos" filtramos la info entregada por conagua para obtener los datos del clima.

Finalmente se manda la info al correo selecionado.

Un detalle importante a tomar en cuenta es que la API de conagua entrega un estatus 403 si no se manda la solicitud con headers, por dicha razon se utilizaron en el programa. Dichos headers los tome/copie de un explorador firefox.