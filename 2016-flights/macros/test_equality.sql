-- C/O https://www.startdataengineering.com/post/how-to-test-sql-using-dbt/

{% macro test_equality(model) %} -- macro definition

{% set compare_model = kwargs.get('compare_model') %} -- get compare_model input parameter
{% set env = kwargs.get('env') %} -- get env input parameter

{%- if target.name == env -%} -- check if env input parameter matches the current environment

select count(*) from ((select * from {{ model }} except select * from {{ compare_model }} )  union (select * from {{ compare_model }} except select * from {{ model }} )) tmp

{%- else -%}

select 0 -- if no input or different env return true

{%- endif -%}

{% endmacro %}
