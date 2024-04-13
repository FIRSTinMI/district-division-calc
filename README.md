# district-division-calc

## Disclaimers

*This tool has been last updated to match rules defined in the **2024** FRC game manual.*

This tool has been created to validate division assignments or generate possible assignments. Its existence does not guarantee that this tool will be used for any particular event. Division generation methodology is at the discretion of event staff and FIRST HQ. If you have questions about schedule or division assignments contact your event's Event Coordinator.

If you see any problems with the algorithm in this tool, this repo welcomes outside contributions or creation of issues.

## Generate Divisions

```bash
python generate_divisions.py --divisions-file test_data/divisions.txt --out-file test_data/out.txt --district FIM --api-key "username:guid" --num-teams 160 --accommodations-file test_data/accommodations.txt --season 2024
```

## Validate Generated Divisions

```bash
python validate_divisions.py --out-file test_data/out.txt --season 2024 --district FIM --api-key "username:guid" --num-teams 160
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

### out.txt
```plaintext
Sponsor A
1

Sponsor C
2
```
