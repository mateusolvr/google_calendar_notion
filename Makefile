.PHONY: run
run: ##@development Build and run environment in background.
	docker run --rm \
	-e DATABASE_ID=${DATABASE_ID} \
	-e COMPANY_EMAIL=${COMPANY_EMAIL} \
	-e CALENDAR_ID=${CALENDAR_ID} \
	-e NOTION_TOKEN=${NOTION_TOKEN} \
	$$(docker build -q -t google-calendar-notion -f ${PWD}/Dockerfile ${PWD}) \
	&& docker image rm google-calendar-notion