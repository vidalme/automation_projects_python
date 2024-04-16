#!/bin/bash

DEFAULT_COMMIT_MESSAGE='Exercicio finalizado ou refeito'

git add .

if [[ ${#} == 0 ]]
then
	git commit -m "${DEFAULT_COMMIT_MESSAGE}"
else
	git commit -m "Exercicio(s) ${@} foram finalizados"
fi

git push