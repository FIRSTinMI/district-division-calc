# district-division-calc

*This tool has been last updated to match rules defined in the **2023** FRC game manual.*

## Run It

```bash
python generate_divisions.py --divisions-file test_data/divisions.txt --out-file test_data/out.txt --district FIM --api-key "username:guid" --num-teams 160 --accommodations-file test_data/accommodations.txt --season 2023
```

## File Formats

### districts.txt

```plaintext
Sponsor A
Sponsor B
Sponsor C
Sponsor D
```

### accommodations.txt

```plaintext
1,Sponsor A,Sponsor D
2,Sponsor C
```
