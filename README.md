# Proyecto_Final-NicolasOsa
El proyecto está hecho en Python y Django haciendo uso de todo lo aprendido en clase. 
El proyecto en sí es la web de una clínica (Clínica Tandil) donde hay algunas funciones que se pueden realizar sin necesidad de generar un usuario. Estas son:
Home: donde se ve la presentación de la clínica y se puede generar un usuario o iniciar sesión.
Plantilla: donde puede ver la plantilla de médicos que hay en la clínica.
Contacto: donde puede escribir un mensaje que será leído por las secretarias.
Los usuarios pueden editar su perfil. Y agregar sus datos personales y un ‘Avatar’.
Al generar un usuario, este será de la categoría Paciente. Aunque Hay dos tipos más de usuarios que solo pueden ser generados por el superusuario, estos son: Medico y Secretaria.
Los ‘Pacientes’ la única funcionalidad que tienen es revisar los turnos que tienen asignados (con que médico, día y hora) en ‘Turnos’.
Las ‘Secretarias’ pueden leer los mensajes que se has dejado en ‘Contacto’. Y en ‘Turnos’ pueden dar los turnos (día, horario, paciente y medico). Y pueden ver los turnos de todos los ‘Pacientes’ y ‘Médicos’. 
Por su lado, los ‘Médicos’ pueden ver los turnos de sus pacientes en ‘Turnos’. Y se les agrega una pestaña que solo pueden ver ellos: ‘Pacientes’. En ella están todos los pacientes y haciendo ‘click’ en el botón Historia clínica pueden ver todos los diagnósticos que tubo el paciente. Además, puede agregar un nuevo diagnóstico. 
