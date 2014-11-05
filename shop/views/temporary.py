## Mako can find this base file because it's in the settings.py -> MAKO_TEMPLATES_DIRS list
<%inherit file="base.htm" />

<%block name="title">
  Stores
 </%block>

 
<%block name="content">

	<table class = "table table-striped table-hover">
		<thead>
			<tr>
				%for key, value in objects[0].variables().items():
					<td>${key}</td>
				%endfor			
			</tr>
		</thead>
		<tbody>
			<tr>
				%for q in objects:
					%for key, value in q.variables().items():
					<td>${value}</td>
					%endfor
				%endfor
			</tr>
		</tbody>
	</table>

 </%block>