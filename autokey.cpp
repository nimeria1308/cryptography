#include <iostream>
#include <cstdlib>

using namespace std;

template <size_t key_size, size_t text_size, bool encode>
static inline void autokey(
    const char *key,
    const char *input, char *output)
{
    // key needs to be writable
    // and is like a ring buffer
    char local_key[key_size];
    // convert to range 0..25
    for (size_t i = 0; i < key_size; i++)
    {
        local_key[i] = key[i] - 'A';
    }

    // go over the input
    for (size_t i = 0; i < text_size; i++)
    {
        // get input
        char c_in = (*input++) - 'A';

        // get current key position
        char *key_pointer = &local_key[i % key_size];

        // key already in range 0..25
        char z = *key_pointer;

        // compute output
        char c_out = ((encode ? (c_in + z) : (c_in + 26 - z)) % 26);

        // write output
        *output++ = c_out + 'A';

        // store plain_text into key
        *key_pointer = encode ? c_in : c_out;
    }
}

int main()
{
    constexpr size_t text_size = 21;
    const char *plain_text = "THEPATHOFTHERIGHTEOUS";
    const char *cipher_text = "FHCIHXWOYAVJKPKYBKVNW";

    constexpr size_t key_size = 3;
    const char *key = "MAY";

    char cipher_text_reconstructed[text_size + 1] = {0};
    char plain_text_reconstructed[text_size + 1] = {0};

    // encode
    autokey<key_size, text_size, true>(key, plain_text, cipher_text_reconstructed);
    cout << plain_text << " -> " << cipher_text_reconstructed << endl;

    // decode
    autokey<key_size, text_size, false>(key, cipher_text, plain_text_reconstructed);
    cout << cipher_text << " -> " << plain_text_reconstructed << endl;

    return 0;
}