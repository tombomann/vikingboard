# VikingBoard

[![KiCad ERC/DRC](https://github.com/tombomann/vikingboard/actions/workflows/kicad-checks.yml/badge.svg)](https://github.com/tombomann/vikingboard/actions/workflows/kicad-checks.yml)

Et modulært elektronikkutviklingsboard med integrert støtte for trådløs kommunikasjon, GPS og utvidbar I/O.

## 📋 Oversikt

VikingBoard er et hardware-prosjekt som kombinerer flere kommunikasjonsmoduler på én plattform:

- **LoRa**: Langdistanse trådløs kommunikasjon
- **CC1101**: Sub-1GHz RF-transceiver
- **NRF24L01**: 2.4GHz trådløs kommunikasjon
- **GPS**: Posisjonering og tidsynkronisering
- **I2C/SPI**: Utvidbare grensesnitt for sensorer og periferiutstyr

## 🎯 Nåværende Status

### Aktive Utviklingsoppgaver

1. **[98-Pin Expansion](https://github.com/tombomann/vikingboard/issues/1)** - Utvide til full 98-pin versjon
2. **[CI/CD Automatisering](https://github.com/tombomann/vikingboard/issues/2)** - GitHub Actions for ERC/DRC
3. **[Footprint Migrering](https://github.com/tombomann/vikingboard/issues/3)** - Bytte til ekte modul-footprints

### Prosjektstatus

- ✅ Initial schematic design
- ✅ PCB layout (preliminary)
- ✅ CI/CD workflow implementert
- 🚧 98-pin spesifikasjon under utvikling
- 🚧 Footprint-migrering planlagt
- ⏳ Prototype testing pending

## 📁 Prosjektstruktur

```
vikingboard/
├── .github/
│   └── workflows/
│       └── kicad-checks.yml    # Automatisk ERC/DRC testing
├── docs/
│   ├── vikingboard_nets.md     # Pin-mapping dokumentasjon
│   ├── vikingboard_98pin_spec.md  # 98-pin expansion spec
│   └── footprint_inventory.md  # Footprint migration tracking
├── kicad/
│   ├── Vikingboard.kicad_sch   # Hovedschematic
│   ├── Vikingboard.kicad_pcb   # PCB layout
│   └── Vikingboard.kicad_pro   # Prosjektfil
├── pcb_scripts/                # Automatiseringsskript
└── tools/                      # Diverse verktøy
```

## 🚀 Kom i gang

### Forutsetninger

- [KiCad 8.0+](https://www.kicad.org/download/)
- Python 3.8+ (for automatiseringsskript)
- Git

### Åpne prosjektet

```bash
git clone https://github.com/tombomann/vikingboard.git
cd vikingboard
kicad kicad/Vikingboard.kicad_pro
```

### Kjør ERC/DRC lokalt

```bash
# Electrical Rule Check
kicad-cli sch erc \
  --output kicad/erc_report.txt \
  kicad/Vikingboard.kicad_sch

# Design Rule Check
kicad-cli pcb drc \
  --output kicad/drc_report.txt \
  kicad/Vikingboard.kicad_pcb
```

## 📖 Dokumentasjon

- **[Pin Mapping](docs/vikingboard_nets.md)** - Komplett oversikt over pins og nett
- **[98-Pin Spec](docs/vikingboard_98pin_spec.md)** - Spesifikasjon for 98-pin utvidelse
- **[Footprint Inventory](docs/footprint_inventory.md)** - Status for footprint-migrering

## 🔧 Utvikling

### Branch-strategi

- `main` - Stabil versjon med fungerende design
- `develop` - Utviklingsgren for nye features
- `feature/*` - Feature branches (f.eks. `feature/lora-module`)
- `footprint/*` - Footprint replacement branches

### Bidra

1. Fork prosjektet
2. Opprett feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit endringer (`git commit -m 'Add some AmazingFeature'`)
4. Push til branch (`git push origin feature/AmazingFeature`)
5. Åpne Pull Request

Alle PRs blir automatisk testet med ERC/DRC sjekker.

## 🗺️ Roadmap

### Fase 1: Foundation (Current)
- [x] Initial design og schematic
- [x] CI/CD oppsett
- [ ] Komplett 98-pin spesifikasjon
- [ ] Footprint-migrering

### Fase 2: Validation
- [ ] Design review
- [ ] Prototype bestilling
- [ ] Hardware testing
- [ ] Dokumentasjon oppdatering

### Fase 3: Production
- [ ] Design freeze
- [ ] Bill of Materials (BOM) finalisering
- [ ] Produksjonsklare filer (Gerber, drill files)
- [ ] Assembly dokumentasjon

## 📊 Hardware Spesifikasjoner

### RF Modules
- **LoRa**: 433/868/915 MHz (region dependent)
- **CC1101**: 300-348, 387-464, 779-928 MHz
- **NRF24L01+**: 2.4 GHz ISM band

### Interfaces
- **Power**: 5V system, 3.3V I/O
- **Communication**: SPI, I2C, UART
- **GPIO**: Utvidbar via Flipper Zero-kompatibel header

### Physical
- **Dimensions**: TBD
- **Layers**: 2-4 layer PCB (TBD)
- **Connectors**: JST/Molex (TBD)

## 🤝 Support

Har du spørsmål eller problemer?

- Åpne en [issue](https://github.com/tombomann/vikingboard/issues)
- Se [dokumentasjonen](docs/)
- Sjekk [eksisterende issues](https://github.com/tombomann/vikingboard/issues?q=is%3Aissue)

## 📝 Lisens

Prosjektet er open source. Lisens TBD.

## 🙏 Acknowledgments

- KiCad-fellesskapet for utmerkede verktøy
- Open source hardware-bevegelsen
- Alle bidragsytere

---

**Note**: Dette prosjektet er under aktiv utvikling. Hardware-design og spesifikasjoner kan endre seg.
