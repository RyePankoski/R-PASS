# R-GEN96

Named a such as my name is Rye, its a generator, and I was born in 96. 

Rye-Generator 96

<img width="614" height="591" alt="image" src="https://github.com/user-attachments/assets/ec874f10-fb39-48f8-9d09-9bd6199f8eaf" />

A dual-mode password generator with cryptographically secure random generation and real-time entropy visualization.

## Features

**Two Generation Modes:**
- **Random Mode**: Generates passwords using printable ASCII characters (33-126)
- **Passphrase Mode**: Generates diceware-style passphrases using the EFF long wordlist (7,776 words)

**Security:**
- Uses Python's `secrets` module for cryptographically secure randomness
- Real-time entropy calculation displayed in bits
- Visual strength indicator with color-coded bar (red to green)

**Passphrase Customization:**
- Separator options: hyphens, spaces, none, or mixed (random selection)
- Configurable word count

**Privacy:**
- No caching or storage of generated passwords
- Strictly output-only operation
- All generation happens locally

## Installation

### Using the Executable (Windows)

Download and run `R-GEN96 v1.2.exe` - no installation required.

### Running from Source

Requires Python 3.x with tkinter (included in standard library).

```bash
python main.py
```

## Usage

1. **Select Mode**: Toggle between Random and Passphrase generation
2. **Set Length**: Enter desired number of characters (Random) or words (Passphrase)
3. **Configure Format** (Passphrase only): Choose separator style
4. **Generate**: Click "Generate Password"
5. **Copy**: Click "Copy" to copy password to clipboard

The strength indicator updates automatically, showing entropy in bits and a visual representation of password strength.

## Entropy Calculation

- **Random passwords**: Based on character set diversity (lowercase, uppercase, digits, symbols) and length
- **Passphrases**: Calculated as `log₂(7776) × number_of_words`

Strength levels:
- Weak: < 28 bits
- Fair: 28-35 bits
- Good: 36-59 bits
- Strong: 60-127 bits
- Very Strong: ≥ 128 bits

## Technical Details

- Built with tkinter, styled with a Windows 95 aesthetic
- EFF long wordlist for passphrase generation
- Printable ASCII range: characters 33-126 (94 total characters)

## Building

To build the executable from source:

```bash
pyinstaller "R-GEN96 v1.2.spec"
```

## License

See repository for license information.
