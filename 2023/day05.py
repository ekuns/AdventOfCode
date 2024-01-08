from os import path


with open('inputs/input05.txt', 'r') as f:
    full_input_lines = f.readlines()
full_input_lines = [l.strip() for l in full_input_lines]
print(f'Number of lines: {len(full_input_lines)}')


# ================ Part 1 ================


def read_maps(lines):
    seeds = [int(x) for x in lines[0].split(':')[1].split()]
    print(f'Seeds: {seeds}')

    maps = {}
    offset = 2
    while offset < len(lines):
        map_name = lines[offset][0:-5]
        offset += 1
        current_list = []
        while offset < len(lines) and lines[offset]:
            current_list.append([int(x) for x in lines[offset].split()])
            offset += 1
        offset += 1
        maps[map_name] = sorted(current_list, key=lambda x: x[1])
    return seeds, maps


def get_mapping(item, next_map):
    for dest, origin, length in next_map:
        # print(f'Looking for {item} in range {origin} to {origin+length-1}')
        if item < origin:
            # print(f'Item {item} is between ranges so returning it unchanged')
            return item, origin - item
        if origin <= item < origin + length:
            # print(f'found {item} in range, returning {item - origin + dest}')
            return item - origin + dest, origin + length - item
    # print(f'Item {item} after end so returning it unchanged')
    return item, None


def get_location(seed, maps):
    soil, soil_range = get_mapping(seed, maps['seed-to-soil'])
    # print(f'Seed {seed} soil is at {soil} with range {soil_range}')
    fertilizer, fertilizer_range = get_mapping(soil, maps['soil-to-fertilizer'])
    # print(f'Seed {seed} fertilizer is at {fertilizer} with range {fertilizer_range}')
    water, water_range = get_mapping(fertilizer, maps['fertilizer-to-water'])
    # print(f'Seed {seed} water is at {water} with range {water_range}')
    light, light_range = get_mapping(water, maps['water-to-light'])
    # print(f'Seed {seed} light is at {light} with range {light_range}')
    temperature, temperature_range = get_mapping(light, maps['light-to-temperature'])
    # print(f'Seed {seed} temperature is at {temperature} with range {temperature_range}')
    humidity, humidity_range = get_mapping(temperature, maps['temperature-to-humidity'])
    # print(f'Seed {seed} humidity is at {humidity} with range {humidity_range}')
    location, location_range = get_mapping(humidity, maps['humidity-to-location'])
    # print(f'Seed {seed} location is {location} with range {location_range}')
    ranges = [soil_range, fertilizer_range, water_range, light_range, temperature_range, humidity_range, location_range]
    ranges = [r for r in ranges if r]
    return location, min(ranges)


def part1(lines):
    seeds, maps = read_maps(lines)
    locations = [get_location(seed, maps) for seed in seeds]
    locations = [l[0] for l in locations]
    first_location = min(locations)
    print(f'The closest seed is at location {first_location}')


# ================ Part 2 ================


def part2(lines):
    seeds, maps = read_maps(lines)
    all_locations = []
    print(f'Checking {len(seeds)//2} collections of seeds...')
    for start_seed, length in zip(seeds[0::2], seeds[1::2]):
        # print(f'Checking {length:,} seeds starting with {start_seed:,} ...')
        offset = 0
        while offset < length:
            # print(f'Checking seed {start_seed+offset:,}')
            location, range_length = get_location(start_seed+offset, maps)
            # print(f'Range length = {range_length:,}')
            all_locations.append(location)
            offset += range_length
    print(f'The closest seed is at location {min(all_locations)}')


if path.isfile('inputs/test05.txt'):
    with open('inputs/test05.txt', 'r') as f:
        test_input_lines = f.readlines()
        test_input_lines = [l.strip() for l in test_input_lines]
        print('\nTEST INPUT PART 1')
        part1(test_input_lines)

if path.isfile('inputs/test05.txt'):
    with open('inputs/test05.txt', 'r') as f:
        test_input_lines = f.readlines()
        test_input_lines = [l.strip() for l in test_input_lines]
        print('\nTEST INPUT PART 2')
        part2(test_input_lines)

print('\nFULL INPUT')
part1(full_input_lines)
part2(full_input_lines)
