from collections import deque
import numpy as np

def infection_projector(params):
    population,R0,asymptomatic_period,hospitalization_rate,inflection_point,R0_reduction,base_R0,hospital_days = params.values()
    day = 0
    total_infections = population
    current_infections = population
    hospitalized_patients = deque(maxlen=hospital_days)
    while 1:
        if day < inflection_point*asymptomatic_period:
            current_infections = R0 * current_infections
            total_infections += current_infections
            day += asymptomatic_period
            hospitalized_patients.append(current_infections * hospitalization_rate)
    #         print(f'hospitalized_patients {sum(hospitalized_patients)}')
        else:
            current_infections = R0 * current_infections
            total_infections += current_infections
            day += asymptomatic_period
            hospitalized_patients.append(current_infections * hospitalization_rate)
            R0 += (base_R0 - R0) / 2
            R0 = max(R0,base_R0)
        if params['print'] == True:
            print(f'Day {day}, Current_infections: {current_infections:.0f}, total_infections: {total_infections:.0f}, Hospitalized_patients {sum(hospitalized_patients):.2f}, R0 {R0:.2f}')
        yield (day,current_infections,total_infections,sum(hospitalized_patients),R0)
    
def advanced_projector(params):
    population,R0,asymptomatic_period,hospitalization_rate,inflection_point,R0_reduction,base_R0,hospital_days,tests,pos_rate,traveler_cases,print_bool = params.values()
    day = 0
    down_day = 0
    total_confirmed = 0
    daily_confirmed = 0
    total_tests = 0
    current_tests = 0
    total_infections = population
    current_infections = population
    hospitalized_patients = deque(maxlen=hospital_days)
    while 1:
        if day < inflection_point*asymptomatic_period:
            current_infections = R0 * current_infections
            total_infections += current_infections
            day += asymptomatic_period
            hospitalized_patients.append(current_infections * hospitalization_rate)
        else:
            current_infections = R0 * current_infections + (traveler_cases * asymptomatic_period)
            total_infections += current_infections
            day += asymptomatic_period
            down_day += asymptomatic_period
            hospitalized_patients.append(current_infections * hospitalization_rate)
            R0 += (base_R0 - R0) / 2
            R0 = max(R0,base_R0)
            current_tests = tests[down_day]
            total_tests += current_tests
            daily_confirmed = current_tests * pos_rate
            total_confirmed += daily_confirmed
        if print_bool == True:
            print(f'Day {day}, Total tests {total_tests:.0f}, Daily_tests {current_tests:.0f}, Daily confirmed {daily_confirmed:.0f}, Total confirmed {total_confirmed:.0f}, Current_infections: {current_infections:.0f}, total_infections: {total_infections:.0f}, Hospitalized_patients {sum(hospitalized_patients):.0f}, R0 {R0:.2f}')
        yield (day,current_infections,total_infections,sum(hospitalized_patients),R0,daily_confirmed,total_confirmed,current_tests,total_tests)

def daily_projector(params):
    population,R0,asymptomatic_period,hospitalization_rate,inflection_point,R0_reduction,base_R0,hospital_days,tests,pos_rate,traveler_cases,print_bool,iterations = params.values()
    R0s,hospitalizations = np.zeros(iterations),np.zeros(iterations)
    down_day = 0
    total_confirmed = np.zeros(iterations)
    daily_confirmed = 0
    total_tests = np.zeros(iterations)
    current_tests = 0
    total_infections = population
    current_infections = population
    hospitalized_patients = deque(maxlen=hospital_days)
    total_infections = np.zeros(iterations)
    total_infections[0] = population
    total_infections[1:1+asymptomatic_period] = (population * R0) / asymptomatic_period
    hospitalized_patients.append(population * hospitalization_rate)
    hospitalizations[0] = sum(hospitalized_patients)
    R0s[0] = R0
    for i in range(1,iterations-3):
        if i < inflection_point:
            total_infections[i] += total_infections[i-1]
            total_infections[i+1:asymptomatic_period+i+1] += (total_infections[i] - total_infections[i-1]) * R0 / asymptomatic_period
            print(total_infections[i])
            print(total_infections[i+1:asymptomatic_period+i+1])
            hospitalized_patients.append((total_infections[i] - total_infections[i-1]) * hospitalization_rate)
            hospitalizations[i] = sum(hospitalized_patients)
            R0s[i] = R0
        else:
            total_infections[i] += total_infections[i-1]
            current_infections = total_infections[i] - total_infections[i-1]
            total_infections[i+1:asymptomatic_period+i+1] += ((current_infections + traveler_cases) * R0 / asymptomatic_period)
            hospitalized_patients.append(current_infections * hospitalization_rate)
            print(total_infections[i])
            print(total_infections[i+1:asymptomatic_period+i+1])
            R0 += (base_R0 - R0) / 2
            R0 = max(R0,base_R0)
            current_tests = tests[down_day]
            total_tests[i] = current_tests + total_tests[i-1]
            daily_confirmed = current_tests * pos_rate
            total_confirmed[i] = daily_confirmed + total_confirmed[i-1]
            down_day += 1
            R0s[i] = R0
            hospitalizations[i] = sum(hospitalized_patients)
        if print_bool == True:
            print(f'Day {i}, Total tests {total_tests:.0f}, Daily_tests {current_tests:.0f}, Daily confirmed {daily_confirmed:.0f}, Total confirmed {total_confirmed:.0f}, Current_infections: {current_infections:.0f}, total_infections: {total_infections:.0f}, Hospitalized_patients {sum(hospitalized_patients):.0f}, R0 {R0:.2f}')
    for j in range(i,iterations):
        total_infections[j] += total_infections[j-1]
        total_infections[j+1:iterations-j] += (total_infections[j] + total_infections[j-1]) * R0 / (iterations-j)
        hospitalized_patients.append((total_infections[j] - total_infections[j-1]) * hospitalization_rate)
        hospitalizations[j] = sum(hospitalized_patients)
        current_tests = tests[j]
        total_tests[j] = current_tests + total_tests[j-1]
        daily_confirmed = current_tests * pos_rate
        total_confirmed[j] = daily_confirmed + total_confirmed[j-1]
        R0 += (base_R0 - R0) / 2
        R0 = max(R0,base_R0)
        R0s[j] = R0
    return (total_infections,hospitalizations,R0s,total_confirmed,total_tests)
    