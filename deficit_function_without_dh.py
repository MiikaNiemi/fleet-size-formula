from itertools import chain

# EXAMPLE DATA SET, DEPARTURE AND ARRIVAL TIMES IN MINUTES
trips = {'AB1': {'dep_time': 560, 'arr_time': 695, 'dep_city': 'Terminal A', 'arr_city': 'Terminal B'},
         'AB2': {'dep_time': 740, 'arr_time': 875, 'dep_city': 'Terminal A', 'arr_city': 'Terminal B'},
         'AB3': {'dep_time': 830, 'arr_time': 965, 'dep_city': 'Terminal A', 'arr_city': 'Terminal B'},
         'AB4': {'dep_time': 920, 'arr_time': 1055, 'dep_city': 'Terminal A', 'arr_city': 'Terminal B'},
         'AB5': {'dep_time': 980, 'arr_time': 1115, 'dep_city': 'Terminal A', 'arr_city': 'Terminal B'},
         'AB6': {'dep_time': 1040, 'arr_time': 1175, 'dep_city': 'Terminal A', 'arr_city': 'Terminal B'},
         'AB7': {'dep_time': 1100, 'arr_time': 1235, 'dep_city': 'Terminal A', 'arr_city': 'Terminal B'},
         'AB8': {'dep_time': 1190, 'arr_time': 1325, 'dep_city': 'Terminal A', 'arr_city': 'Terminal B'},
         'BA1': {'dep_time': 540, 'arr_time': 675, 'dep_city': 'Terminal B', 'arr_city': 'Terminal A'},
         'BA2': {'dep_time': 630, 'arr_time': 765, 'dep_city': 'Terminal B', 'arr_city': 'Terminal A'},
         'BA3': {'dep_time': 720, 'arr_time': 855, 'dep_city': 'Terminal B', 'arr_city': 'Terminal A'},
         'BA4': {'dep_time': 810, 'arr_time': 945, 'dep_city': 'Terminal B', 'arr_city': 'Terminal A'},
         'BA5': {'dep_time': 900, 'arr_time': 1035, 'dep_city': 'Terminal B', 'arr_city': 'Terminal A'},
         'BA6': {'dep_time': 990, 'arr_time': 1125, 'dep_city': 'Terminal B', 'arr_city': 'Terminal A'},
         'BA7': {'dep_time': 1080, 'arr_time': 1215, 'dep_city': 'Terminal B', 'arr_city': 'Terminal A'},
         'BA8': {'dep_time': 1140, 'arr_time': 1275, 'dep_city': 'Terminal B', 'arr_city': 'Terminal A'},
         'CA1': {'dep_time': 570, 'arr_time': 710, 'dep_city': 'Terminal C', 'arr_city': 'Terminal A'},
         'CA2': {'dep_time': 740, 'arr_time': 880, 'dep_city': 'Terminal C', 'arr_city': 'Terminal A'},
         'CA3': {'dep_time': 860, 'arr_time': 1000, 'dep_city': 'Terminal C', 'arr_city': 'Terminal A'},
         'CA4': {'dep_time': 920, 'arr_time': 1060, 'dep_city': 'Terminal C', 'arr_city': 'Terminal A'},
         'CA5': {'dep_time': 1040, 'arr_time': 1180, 'dep_city': 'Terminal C', 'arr_city': 'Terminal A'},
         'AC1': {'dep_time': 555, 'arr_time': 695, 'dep_city': 'Terminal A', 'arr_city': 'Terminal C'},
         'AC2': {'dep_time': 675, 'arr_time': 815, 'dep_city': 'Terminal A', 'arr_city': 'Terminal C'},
         'AC3': {'dep_time': 795, 'arr_time': 935, 'dep_city': 'Terminal A', 'arr_city': 'Terminal C'},
         'AC4': {'dep_time': 1155, 'arr_time': 1295, 'dep_city': 'Terminal A', 'arr_city': 'Terminal C'},
         'AC5': {'dep_time': 1215, 'arr_time': 1355, 'dep_city': 'Terminal A', 'arr_city': 'Terminal C'},
         'AD1': {'dep_time': 560, 'arr_time': 770, 'dep_city': 'Terminal A', 'arr_city': 'Terminal D'},
         'DA1': {'dep_time': 860, 'arr_time': 1070, 'dep_city': 'Terminal D', 'arr_city': 'Terminal A'},
         'CD1': {'dep_time': 450, 'arr_time': 720, 'dep_city': 'Terminal C', 'arr_city': 'Terminal D'},
         'DC1': {'dep_time': 810, 'arr_time': 1080, 'dep_city': 'Terminal D', 'arr_city': 'Terminal C'}}

# TERMINALS AND MINIMUM INTERVALS BETWEEN TRIPS
terminals = {'Terminal A': {'min_interval': 40},
             'Terminal B': {'min_interval': 15},
             'Terminal C': {'min_interval': 20},
             'Terminal D': {'min_interval': 30}}

t0 = min(x['dep_time'] for x in trips.values())
t1 = max(x['arr_time'] for x in trips.values())


def count_df(t_min=t0, t_max=t1):

    # TOTAL PEAK VEHICLE REQUIREMENT
    pvr = 0

    # LIST FOR INITIAL IDS
    initial_ids = []

    for t in terminals:

        # DEFICIT BY TERMINAL
        df = 0

        dep_times = sorted(v['dep_time'] for k, v in trips.items() if v['dep_city'] == t)
        arr_times = sorted(v['arr_time'] for k, v in trips.items() if v['arr_city'] == t)

        for minute in range(t_min, t_max+1):

            # DEFICIT BY MINUTE
            dep_amount = len(list(filter(lambda x: x <= minute, dep_times)))
            arr_amount = len(list(filter(lambda x: x <= minute - terminals[t]['min_interval'], arr_times)))
            difference = dep_amount - arr_amount

            # IF DEFICIT EXCEEDS PREVIOUS MAX, VEHICLE REQUIREMENT INCREASES
            if difference > df:
                # DEPARTURES BY MINUTE AND INCREASE REQUIREMENT ARE NOT NECESSARILY THE SAME
                add_amount = difference - df
                # SORTING IS OPTIONAL
                trip_ids = sorted(list(k for k, v in trips.items() if v['dep_city'] == t and v['dep_time'] == minute),
                                  key=lambda x: trips[x]['arr_time'] - trips[x]['dep_time'], reverse=True)
                initial_ids.extend(trip_ids[:add_amount])

                df = difference

        pvr += df

    # NUMBER OF UNIQUE INITIAL IDS MUST MATCH WITH VEHICLE REQUIREMENT
    if len(set(initial_ids)) == pvr:
        return initial_ids


def construct_blocks():

    # VEHICLE ROWS ARE CREATED STARTING WITH INITIAL TRIPS
    first_blocks_starts = count_df()
    vehicle_blocks = [[x] for x in first_blocks_starts]

    for t in terminals:

        departures = sorted(list(k for k, v in trips.items() if
                                 v['dep_city'] == t and
                                 k not in first_blocks_starts), key=lambda x: trips[x]['dep_time'])

        arrivals = sorted(list(k for k, v in trips.items() if
                               v['arr_city'] == t), key=lambda x: trips[x]['arr_time'])

        # IF THERE ARE DEPARTURES, ARRIVAL-DEPARTURE -PAIRS ARE CREATED
        if departures:
            for d in range(len(departures)):

                block_starts = list(x[0] for x in vehicle_blocks)
                block_ends = list(x[-1] for x in vehicle_blocks)
                start_index = block_starts.index(departures[d]) if departures[d] in block_starts else None
                end_index = block_ends.index(arrivals[d]) if arrivals[d] in block_ends else None

                # IF DEPARTURE AND ARRIVAL ARE ALREADY HANDLED EARLIER, BLOCKS ARE JOINED TOGETHER
                if departures[d] in block_starts and arrivals[d] in block_ends:
                    vehicle_blocks[end_index].extend(vehicle_blocks.pop(start_index))

                # IF DEPARTURE IS ALREADY HANDLED, ARRIVAL IS INSERTED BEFORE THE DEPARTURE
                elif departures[d] in block_starts and arrivals[d] not in block_ends:
                    vehicle_blocks[start_index].insert(0, arrivals[d])

                # IF ARRIVAL IS ALREADY HANDLED, DEPARTURE IS APPENDED AFTER THE ARRIVAL
                elif departures[d] not in block_starts and arrivals[d] in block_ends:
                    vehicle_blocks[end_index].append(departures[d])

                # IF NEITHER IS ALREADY HANDLED, A TEMPORARY ROW IS CREATED TO BE JOINED LATER
                elif departures[d] not in block_starts and arrivals[d] not in block_ends:
                    vehicle_blocks.append([arrivals[d], departures[d]])

    trips_in_vehicle_blocks = sorted(chain.from_iterable(vehicle_blocks))
    scheduled_trips = sorted(trips.keys())

    if trips_in_vehicle_blocks == scheduled_trips and first_blocks_starts == list(x[0] for x in vehicle_blocks):
        for b in range(len(vehicle_blocks)):
            print(f'Vehicle {b+1}: {vehicle_blocks[b]}')
        print()
        print(f'Peak vehicle requirement: {len(first_blocks_starts)}')


construct_blocks()
