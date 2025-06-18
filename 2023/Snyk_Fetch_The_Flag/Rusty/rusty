use std::fs;

const CHARSET: &[u8] = b"QWlKoxp3mT9EeRb4YzgG6rNj1OLvZ5SDfMBaXtP8JyIFVH07uh2wicdnUAC#@q";

fn main() {
    let content = fs::read_to_string("flag.txt").expect("Unable to read flag.txt");

    let input = content.as_bytes();
    let mut output = Vec::new();

    let mut temp = 0u32;
    let mut temp_len = 0u8;

    for &byte in input {
        temp = (temp << 8) | byte as u32;
        temp_len += 8;

        while temp_len >= 6 {
            temp_len -= 6;
            output.push(CHARSET[((temp >> temp_len) & 0x3F) as usize]);
        }
    }

    if temp_len > 0 {
        output.push(CHARSET[((temp << (6 - temp_len)) & 0x3F) as usize]);
    }

    while output.len() % 4 != 0 {
        output.push(b'=');
    }

    let out = String::from_utf8(output).unwrap();

    println!("{}", out);
}
