.DEFAULT_GOAL := default
#################### PACKAGE ACTIONS ###################
reinstall_package:
	@pip uninstall -y research_topics_ranker || :
	@pip install -e .

run_fetch_data:
	python -m research_topics_ranker.fetch_data




#################### PACKAGE ACTIONS ###################
#reinstall_package:
#	@pip uninstall -y taxifare || :
#	@pip install -e .

#run_preprocess:
#	python -c 'from taxifare.interface.main import preprocess; preprocess()'

#run_train:
#	python -c 'from taxifare.interface.main import train; train()'

#run_pred:
#	python -c 'from taxifare.interface.main import pred; pred()'

#run_evaluate:
#	python -c 'from taxifare.interface.main import evaluate; evaluate()'

#run_all: run_preprocess run_train run_pred run_evaluate
