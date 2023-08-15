# Bot de Verificación y Moderación para Servidores SA-MP

> ¡Bienvenido al repositorio del Bot de Verificación y Moderación para servidores SA-MP! Este bot te permite verificar cuentas de usuarios desde un canal específico en Discord y ofrece funciones adicionales de moderación. Está diseñado para ser adaptable a varios servidores SA-MP que utilicen bases de datos.

## Características

- Verificación de cuentas de usuarios en el servidor SA-MP desde un canal designado.
- Funciones de moderación para mantener un ambiente seguro y ordenado.
- Integración entre tu servidor SA-MP y Discord de manera sencilla.

## Configuración

Sigue estos pasos para poner en marcha el bot en tu servidor:

1. Instala los requisitos necesarios ejecutando el comando `pip install -r requirements.txt`.
2. Configura la conexión MySQL de tu servidor y la dirección IP en el archivo `.env`. Esta configuración es esencial para el correcto funcionamiento del bot.
3. En las líneas (106, 107, 108) del código, establece los ID de los roles en Discord que corresponden a los rangos de administración en tu servidor.
4. En la "línea 134", asegúrate de ingresar el ID del rol asignado a los usuarios verificados.

## Contribuciones

Aunque soy principiante en el desarrollo de bots, he creado esta herramienta con la intención de facilitar la vinculación entre servidores SA-MP y Discord. Si eres un desarrollador experimentado y encuentras áreas de mejora en el código, te invito a contribuir al repositorio. Cualquier actualización o mejora será bienvenida, siempre y cuando mantenga buenas prácticas de programación y no cause problemas.

¡Espero que encuentres este bot útil y que sea de gran ayuda para tu comunidad de SA-MP y Discord! Si tienes alguna pregunta o sugerencia, no dudes en ponerte en contacto.

*Nota: Este README.md está sujeto a cambios y actualizaciones a medida que el bot se desarrolla y mejora.*

## Créditos de Bibliotecas

Agradecemos a las siguientes bibliotecas y proyectos de código abierto por hacer posible este proyecto:

- aiohttp
- aiosignal
- altgraph
- async-timeout
- attrs
- certifi
- cffi
- charset-normalizer
- click
- colorama
- discord
- docopt
- frozenlist
- idna
- multidict
- mysql-connector-python
- pefile
- pipreqs
- protobuf
- py-cord
- pycparser
- pyinstaller
- pyinstaller-hooks-contrib
- PyNaCl
- python-dotenv
- pywin32-ctypes
- requests
- samp-client
- urllib3
- yarg
- yarl
- youtube-dl

## Donaciones

Si encuentras útil este proyecto y deseas apoyar su desarrollo continuo, considera realizar una donación. Cualquier contribución es muy apreciada y nos ayudará a mantener y mejorar este bot.

**PayPal**: [sorac.games@gmail.com](mailto:sorac.games@gmail.com)

¡Gracias por tu generosidad y apoyo!

  *Nota #2: Respetar creditos*
