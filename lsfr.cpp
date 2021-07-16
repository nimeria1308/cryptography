#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <set>

using namespace std;

#if 0
template <typename T>
struct xorshift_state
{
    T a;
};

template <typename T>
T xorshift(struct xorshift_state<T> *state);

template <>
uint16_t xorshift(struct xorshift_state<uint16_t> *state)
{
    /* Algorithm "xor" from p. 4 of Marsaglia, "Xorshift RNGs" */
    uint16_t x = state->a;
    x ^= x >> 7;
    x ^= x << 9;
    x ^= x >> 13;
    return state->a = x;
}

template <>
uint32_t xorshift(struct xorshift_state<uint32_t> *state)
{
    /* Algorithm "xor" from p. 4 of Marsaglia, "Xorshift RNGs" */
    uint32_t x = state->a;
    x ^= x << 13;
    x ^= x >> 17;
    x ^= x << 5;
    return state->a = x;
}

template <typename T>
size_t lfsr_period(T start_state)
{
    size_t period = 0;

    struct xorshift_state<T> state =
    {
        start_state
    };

    while (xorshift<T>(&state) != start_state)
    {
        period++;
    }

    return period;
}

int main()
{
    uint32_t start_state = 0x1; /* Any nonzero start state will work. */
    size_t period = lfsr_period(start_state);

    cout << hex << start_state << ": " << dec << period << endl;

    return 0;
}
#endif

static inline unsigned int pop_count(unsigned int x)
{
    unsigned int c = 0;
    while (x)
    {
        if (x & 1)
        {
            c++;
        }
        x >>= 1;
    }

    return c;
}

template <size_t size>
unsigned int lsfr(unsigned int taps, unsigned int value)
{
    const unsigned int mask = ((1 << size) - 1);

    // shift left
    unsigned int new_value = (value << 1) & mask;

    // cout << bitset<8>(value << 1) << " & " << bitset<8>(mask) << " = " << bitset<8>(new_value) << endl;

    // find new bit
    new_value |= (pop_count(value & taps) % 2);

    return new_value;
}

template <size_t size>
unsigned int find_period(unsigned int taps, unsigned int start_value)
{
    unsigned int current = start_value;
    unsigned int t = 0;
    set<unsigned int> previous { start_value };

    do
    {
        // cout << "t[" << t << "]: ";
        // cout << bitset<size>(current) << " (" << current << ")" << endl;
        current = lsfr<size>(taps, current);
        t++;
    cout << "Comparing " << bitset<8>(start_value) << " vs " << bitset<8>(current) << endl;
        if (current == start_value) {
            cout << "period " << t << ": " << bitset<size>(start_value) << " " << bitset<size>(current) << endl;
            break;
        } else if (previous.count(current)) {
            return 0;
        }
        previous.insert(current);
    } while (true);

    return t;
}

template <size_t size>
void print_periods()
{
    const unsigned int max_value = (1 << size) - 1;

    cout << "Periods for " << size << " taps" << endl;

    unsigned int taps = 43;
    // unsigned int start_value = 1;

    // for (unsigned taps = 1; taps <= max_value; taps++)
    // {
        bool found_period = true;
        unsigned int period = find_period<size>(taps, 1);

    //     if (period)
    //     {
    //         for (unsigned int start_value = 2; start_value <= max_value; start_value++)
    //         {
                // unsigned int p = find_period<size>(taps, start_value);
                // if (p != period)
                // {
                //     found_period = false;
                //     break;
                // }
                // cout << endl;
            // }
        // }
        // else
        // {
        //     found_period = false;
        // }

        if (found_period)
        {
            cout << "taps: " << bitset<size>(taps) << " period: " << period << endl;
        }
        // cout << endl;
    // }

    // cout << endl;
}

int main()
{
    // taps: x0 + x3 = 1001
    // unsigned int taps = (1 << 3) + (1 << 0);
    // unsigned int period = find_period<4>(taps, 1);
    // cout << "period: " << period << endl;

    // print_periods<1>();
    // print_periods<2>();
    // print_periods<3>();
    // print_periods<4>();
    // print_periods<5>();
    print_periods<6>();
    // print_periods<7>();

    unsigned int taps = 43;
    // unsigned int taps = 58;
    unsigned int current = 1;
    for (int t = 0; t < 25; t++) {
        cout << t << ": " << bitset<7>(current) << endl;
        current = lsfr<7>(taps, current);
    }

    return 0;
}