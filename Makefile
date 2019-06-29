.DEFAULT_GOAL := check-aws-environmentvars

check-aws-environmentvars:
ifndef AWS_ACCESS_KEY_ID
	$(error AWS_ACCESS_KEY_ID is not set; \
	please set the variable and try again)
endif

.PHONY: generate-creds-pratham generate-creds-buildserverlessdev
generate-creds-pratham:
	python xaccount-scripts/generate-creds.py --account 640393631002 --role psp-stackset-roles-rAdministratorAccess-191FXW95Z4K17

generate-creds-buildserverlessdev:
	python xaccount-scripts/generate-creds.py --account 345089341006 --role psp-stackset-roles-rAdministratorAccess-FRZCI8DR1FXU