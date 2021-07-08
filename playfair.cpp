#include <cstdlib>

#include <algorithm>
#include <iostream>
#include <string>
#include <sstream>
#include <vector>

using namespace std;

#define PLAYFAIR_KEY_LEN 25
typedef const char playfair_key_t[PLAYFAIR_KEY_LEN];

static inline size_t playfair_get_coords(char c, playfair_key_t key)
{
    size_t x;
    for (x = 0; x < PLAYFAIR_KEY_LEN; x++)
    {
        if (c == key[x])
        {
            break;
        }
    }

    // will be 25 if not found
    return x;
}

template <bool encode>
static inline size_t playfield_get_new_col(size_t col)
{
    if (encode)
    {
        return (col + 1) % 5;
    }
    else
    {
        return col == 0 ? 4 : (col - 1);
    }
}

template <size_t text_len, bool encode>
void playfair(
    playfair_key_t key, const char *plain_text, char *crypt_text)
{
    for (size_t i = 0; i < text_len; i += 2)
    {
        // get pair chars
        const char a = plain_text[i];
        const char b = plain_text[i + 1];

        // get a coords
        const size_t a_coord = playfair_get_coords(a, key);
        const size_t b_coord = playfair_get_coords(b, key);

        size_t a_coord_key;
        size_t b_coord_key;

        if ((a_coord >= PLAYFAIR_KEY_LEN) || (b_coord >= PLAYFAIR_KEY_LEN))
        {
            // if either char not found, don't encode
            crypt_text[i] = '?';
            crypt_text[i + 1] = '?';
            continue;
        }

        const size_t a_col = a_coord % 5;
        const size_t a_row = a_coord / 5;

        const size_t b_col = b_coord % 5;
        const size_t b_row = b_coord / 5;

        if (a_col == b_col)
        {
            // same column
            // return characters down the column
            const ssize_t offset = encode ? 5 : -5;
            a_coord_key = PLAYFAIR_KEY_LEN + a_coord + offset;
            b_coord_key = PLAYFAIR_KEY_LEN + b_coord + offset;
        }
        else if (a_row == b_row)
        {
            // same row
            // return characters down the row
            a_coord_key = a_coord - a_col + playfield_get_new_col<encode>(a_col);
            b_coord_key = b_coord - b_col + playfield_get_new_col<encode>(b_col);
        }
        else
        {
            // rectangle rule
            a_coord_key = (a_coord - a_col) + b_col;
            b_coord_key = (b_coord - b_col) + a_col;
        }

        // lookup in key and write in output
        const char a_crypted = key[a_coord_key % PLAYFAIR_KEY_LEN];
        const char b_crypted = key[b_coord_key % PLAYFAIR_KEY_LEN];

        crypt_text[i] = a_crypted;
        crypt_text[i + 1] = b_crypted;
    }
}

template <size_t text_length>
size_t evaluate_key(const char *plain_text, const char *reconstructed_text)
{
    size_t match = 0;

    for (size_t i = 0; i < text_length; i++)
    {
        // char r = *reconstructed_text++;
        char r = reconstructed_text[i];
        if (r == '?' || r == '_')
        {
            continue;
        }

        char p = plain_text[i];
        if (p != r)
        {
            return 0;
        }

        match++;
    }

    return match;
}

template <size_t text_length, size_t minimum_key_match>
void playfair_make_matrix_(
    vector<string> &keys,
    const string &key,
    const char *cypher_text,
    const char *plain_text,
    char *reconstructed_text,
    const vector<string> &inlines,
    size_t inline_key_number)
{
    const string &current_inline = inlines[inline_key_number];

    // for (int i = 0; i < inline_key_number; i++) {
    //     cout << "  ";
    // }

    // cout << current_inline << "(" << inline_key_number << ")" << endl;

    // try all rows
    for (size_t row = 0; row < 25; row += 5)
    {
        // try all combinations in row
        for (size_t col = 0; col < 5; col++)
        {
            bool has_space = true;

            for (size_t s = 0; s < current_inline.size(); s++)
            {
                size_t cc = row + ((col + s) % 5);
                if (key[cc] != '_')
                {
                    has_space = false;
                }
                break;
            }

            if (has_space)
            {
                // found a free space
                string new_key(key);

                for (size_t s = 0; s < current_inline.size(); s++)
                {
                    size_t cc = row + ((col + s) % 5);
                    new_key[cc] = current_inline[s];
                }

                playfair<text_length, false>(new_key.c_str(), cypher_text, reconstructed_text);
                // size_t key_match = evaluate_key<text_length>(plain_text, reconstructed_text);
                // if (!key_match)
                // {
                //     continue;
                // }

                if (inline_key_number < inlines.size() - 1)
                {
                    // go deeper
                    playfair_make_matrix_<text_length, minimum_key_match>(
                        keys,
                        new_key,
                        cypher_text,
                        plain_text,
                        reconstructed_text,
                        inlines,
                        inline_key_number + 1);
                }
                else
                {
                    // record key
                    // if (key_match >= minimum_key_match)
                    // {
                    //     cout
                    //         << key_match << " "
                    //         << reconstructed_text << " "
                    //         << new_key
                    //         << endl;
                    // }
                    keys.push_back(new_key);
                }
            }
        }
    }

    // try all cols
    for (size_t col = 0; col < 5; col++)
    {
        // try all combinations in col
        for (size_t row = 0; row < 25; row += 5)
        {
            bool has_space = true;

            for (size_t s = 0, rr = 0; s < current_inline.size(); s++, rr += 5)
            {
                size_t cc = (row + col + rr) % PLAYFAIR_KEY_LEN;
                if (key[cc] != '_')
                {
                    has_space = false;
                }
                break;
            }

            if (has_space)
            {
                // found a free space
                string new_key(key);

                for (size_t s = 0, rr = 0; s < current_inline.size(); s++, rr += 5)
                {
                    size_t cc = (row + col + rr) % PLAYFAIR_KEY_LEN;
                    new_key[cc] = current_inline[s];
                }

                playfair<text_length, false>(new_key.c_str(), cypher_text, reconstructed_text);
                // size_t key_match = evaluate_key<text_length>(plain_text, reconstructed_text);
                // if (!key_match)
                // {
                //     continue;
                // }

                if (inline_key_number < inlines.size() - 1)
                {
                    // go deeper
                    playfair_make_matrix_<text_length, minimum_key_match>(
                        keys,
                        new_key,
                        cypher_text,
                        plain_text,
                        reconstructed_text,
                        inlines,
                        inline_key_number + 1);
                }
                else
                {
                    // record key
                    // if (key_match >= minimum_key_match)
                    // {
                    //     cout
                    //         << key_match << " "
                    //         << reconstructed_text << " "
                    //         << new_key
                    //         << endl;
                    // }
                    keys.push_back(new_key);
                }
            }
        }
    }
}

template <size_t text_length, size_t minimum_key_match>
void playfair_make_matrix(
    vector<string> &keys,
    const vector<string> &inlines,
    const char *cypher_text,
    const char *plain_text)
{
    // const string key(PLAYFAIR_KEY_LEN, '_');
    const string key = "NTWZE__U_BA_FOSDGHIR____C";
    char reconstructed_text[text_length + 1] = {0};
    playfair_make_matrix_<text_length, minimum_key_match>(keys, key, cypher_text, plain_text, reconstructed_text, inlines, 0);
}

int main()
{
#if 0
    ostringstream ss;
    // A..S
    //
    for (char c = 'A'; c <= 'L'; c++)
    {
        if (c == 'J')
        {
            continue;
        }

        ss << c;
    }

    string key = ss.str();

    cout << key << ": ";

    // FOS
    // NTW
    // HEIRUDC
    // ABCDEFGHIKLMNOPQRSTUVWXYZ
    // ABCDEGHIKLMPQRUVXYZ
    // ABCDEGHIKLMPQRUVXYZ
    // HEIRUDC____________
    // string keyX = "HEIRUDC____________";
    string keyX = "HEI________________";

    size_t count = 0;
    do
    {
        // cout << key << endl;
        count++;
    } while (next_permutation(keyX.begin(), keyX.end()));

    cout << count << endl;
    // 212 278 963
#endif
#if 1
    const char *key =
        "NTWZE"
        "__U_B"
        "A_FOS"
        "DGHIR"
        "____C";

    // find all variants for FOS and NTW
    // TH TE IS
    // H E I

    const char *plain_text = "THEWINTEROFOURDISCONTENT";
    //                        ??????T_??FO????????T_NT

    // WGNZDZWNISOSBHGRREAZWNTW
    // char cypher_text[25] = {0};
    const char *cypher_text = "WGNZDZWNISOSBHGRREAZWNTW";
    // char reconstructed_text[25] = {0};

    // playfair<24, true>(key, plain_text, cypher_text);
    // playfair<24, false>(key, cypher_text, reconstructed_text);

    // cout << "Plain: '" << plain_text << "'" << endl;
    // cout << "Cypher: '" << cypher_text << "'" << endl;
    // cout << "Reconstructed: '" << reconstructed_text << "'" << endl;

    vector<string> possible_keys;
    vector<string> inlines = {
        "K", "L", "M", "P", "Q", "V", "X", "Y",
        // "FOS",
        // "NTW",
        // "H",
        // "E",
        // "I",
        // "R",
        // "U",
        // "D",
        // "C",
        // "G",
        // "Z",
        // "B",
        // "A",
    };

    playfair_make_matrix<24, 11>(possible_keys, inlines, cypher_text, plain_text);

    // for (size_t i = 0; i < possible_keys.size(); i++)
    // {
    //     // cout << i << endl;
    //     for (size_t k = 0; k < PLAYFAIR_KEY_LEN; k += 5)
    //     {
    //         cout << possible_keys[i].substr(k, 5) << endl;
    //     }

    //     playfair<24, false>(possible_keys[i].c_str(), cypher_text, reconstructed_text);
    //     if (reconstructed_text[0] == 'T') {
    //         cout << reconstructed_text << endl;
    //     }

    //     cout << endl;
    // }

    cout << possible_keys.size() << endl;

    char reconstructed_text[25] = {0};
    for (auto key : possible_keys) {
        playfair<24, false>(key.c_str(), "EBQXZLHDLKIVQGOMALEBVBDOSGSFZRANDAMOLBSEELSOZLKDCOZFGSIN", reconstructed_text);
        cout << reconstructed_text << endl;
    }
#endif

#if 0
    char reconstructed_text[25] = {0};
    playfair<24, false>("NTWZEKLUMBAPFOSDGHIRQVXYC", "WGNZDZWNISOSBHGRREAZWNTW", reconstructed_text);
    cout << reconstructed_text << endl;
#endif
    return 0;
}