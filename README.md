\# ATLAS — Industrial Crisis Response Simulator



ATLAS is a Python-based industrial decision-support prototype that simulates equipment failures in a simplified chemical manufacturing plant and evaluates potential recovery strategies.



The project combines process engineering, financial analysis, and software development to explore how operational disruptions affect production and how recovery decisions change with downtime and economic assumptions.



\## Live Demo



Try ATLAS in your browser:



https://atlas-industrial-simulator.streamlit.app/



\## Features



\- \*\*Equipment failure simulation:\*\* Simulate single or multiple equipment outages.

\- \*\*Process network visualization:\*\* Display equipment connectivity, operating status, and rated capacities.

\- \*\*Production impact analysis:\*\* Estimate available plant capacity, production shortfalls, and revenue at risk.

\- \*\*Recovery strategy evaluation:\*\* Compare modeled recovery alternatives using surviving production, startup delays, contribution margin, and fixed activation costs.

\- \*\*Sensitivity analysis:\*\* Evaluate how recommended strategies change across different disruption durations.

\- \*\*Scenario storage:\*\* Save and retrieve scenarios using SQLite and export results to CSV.

\- \*\*Automated testing:\*\* Unit tests covering plant calculations, recovery logic, simulation integration, scenario storage, and network visualization.



\## Technology Stack



Python, Streamlit, pandas, SQLite, Graphviz, and unittest.



\## Running Locally



Install the dependencies:



```bash

python -m pip install -r requirements.txt

```



Launch the dashboard:



```bash

python -m streamlit run dashboard.py

```



Run the automated tests:



```bash

python -m unittest discover -v

```



On Windows, the `py` launcher can be used instead of `python`.



\## Example Scenario



Consider a plant with a normal production target of 900 kg/hr. A main reactor failure reduces available production to 600 kg/hr.



ATLAS compares the cost of accepting the production shortfall against activating an additional recovery strategy.



Under an illustrative contribution margin of $5/kg:



\- At 8 hours of disruption, no additional recovery is preferred.

\- At 24 hours, temporary processing becomes economically preferable under the modeled assumptions.



The example demonstrates why the optimal response can change with the anticipated duration of a disruption.



\## Modeling Assumptions and Limitations



ATLAS is an educational prototype, not validated industrial control software.



The model uses a simplified production network with fixed equipment capacities, constant production targets, deterministic startup delays, and user-specified economic assumptions.



Recovery options are evaluated individually. The current implementation does not optimize simultaneous interventions, material inventories, process dynamics, quality constraints, uncertain repair times, or detailed material and energy balances.



Estimated financial impact represents lost contribution margin plus modeled recovery activation costs, not a complete financial forecast.



\## Project Objective



ATLAS demonstrates the process of translating an operational problem into a quantitative decision-support application: defining equipment dependencies, modeling constraints, comparing alternatives, testing calculations, and communicating results through an interactive interface.

