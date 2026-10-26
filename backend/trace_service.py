
def get_trace(domain):
    return [
        {
            "stage": "Client",
            "message": f"User requests {domain}",
            "simulated": True
        },
        {
            "stage": "Recursive Resolver",
            "message": "Resolver checks its cache",
            "simulated": True
        },
        {
            "stage": "Root Server",
            "message": "Conceptual referral to the TLD",
            "simulated": True
        },
        {
            "stage": "TLD Server",
            "message": "Conceptual referral to the authoritative server",
            "simulated": True
        },
        {
            "stage": "Authoritative Server",
            "message": "Conceptual authoritative DNS response",
            "simulated": True
        }
    ]
