#include <cstdint>
#include <iostream>

using namespace std;

static inline bool check_params(
    unsigned int a, unsigned int b, unsigned int c, unsigned int d)
{

    const unsigned int bc = b * c;

    return ((((a * a) + bc) % 26) == 1) &&
           (((bc + (d * d)) % 26) == 1) &&
           ((((a * b) + (b * d)) % 26) == 0) &&
           ((((a * c) + (c * d)) % 26) == 0);
}

int main()
{
    size_t count = 0;
    for (unsigned int a = 0; a < 26; a++)
    {
        for (unsigned int b = 0; b < 26; b++)
        {
            for (unsigned int c = 0; c < 26; c++)
            {
                for (unsigned int d = 0; d < 26; d++)
                {
                    if (check_params(a, b, c, d))
                    {
                        count++;
                    }
                }
            }
        }
    }

    cout << "count: " << count << endl;

    return 0;
}
