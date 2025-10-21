for i in {1..10}; do
  python3 generate_scenarios.py training_run_$i.csv testing_run_$i.csv
done
