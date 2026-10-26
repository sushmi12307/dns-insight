
import time
import dns.resolver
import dns.exception

from cache_manager import get_cached, store_cached


RECORD_TYPES = ["A", "AAAA", "CNAME", "MX", "NS", "TXT"]

# Create the DNS resolver
resolver = dns.resolver.Resolver()
resolver.timeout = 2
resolver.lifetime = 4


def lookup(domain, record_type="A"):
    domain = domain.strip().rstrip(".")
    record_type = record_type.upper()

    # Validate the input
    if not domain or len(domain) > 253:
        raise ValueError("Please enter a valid domain name.")

    if any(char.isspace() for char in domain):
        raise ValueError("Domain name must not contain spaces.")

    if record_type not in RECORD_TYPES:
        raise ValueError("Unsupported DNS record type.")

    # Check the application cache first
    cache_key = (domain.lower(), record_type)
    cached_result = get_cached(cache_key)

    if cached_result is not None:
        result = cached_result.copy()
        result["cache_status"] = "HIT"
        result["latency_ms"] = 0
        return result

    # Perform a real DNS query
    start = time.perf_counter()

    try:
        answer = resolver.resolve(
            domain,
            record_type,
            search=False
        )

        ttl = answer.rrset.ttl if answer.rrset else None

        result = {
            "domain": domain,
            "record_type": record_type,
            "records": [record.to_text() for record in answer],
            "ttl": ttl,
            "latency_ms": round(
                (time.perf_counter() - start) * 1000, 2
            ),
            "status": "success",
            "cache_status": "MISS"
        }

        # Store the result for its TTL
        store_cached(cache_key, result, ttl)

        return result

    except dns.resolver.NXDOMAIN:
        return {
            "domain": domain,
            "record_type": record_type,
            "records": [],
            "ttl": None,
            "latency_ms": round(
                (time.perf_counter() - start) * 1000, 2
            ),
            "status": "nxdomain",
            "cache_status": "MISS",
            "message": "The domain does not exist according to DNS."
        }

    except dns.resolver.NoAnswer:
        return {
            "domain": domain,
            "record_type": record_type,
            "records": [],
            "ttl": None,
            "latency_ms": round(
                (time.perf_counter() - start) * 1000, 2
            ),
            "status": "no_answer",
            "cache_status": "MISS",
            "message": "No record of the requested type was found."
        }

    except dns.exception.Timeout:
        return {
            "domain": domain,
            "record_type": record_type,
            "records": [],
            "ttl": None,
            "latency_ms": round(
                (time.perf_counter() - start) * 1000, 2
            ),
            "status": "timeout",
            "cache_status": "MISS",
            "message": "The DNS query timed out."
        }

    except dns.resolver.NoNameservers:
        return {
            "domain": domain,
            "record_type": record_type,
            "records": [],
            "ttl": None,
            "latency_ms": round(
                (time.perf_counter() - start) * 1000, 2
            ),
            "status": "no_nameservers",
            "cache_status": "MISS",
            "message": "No DNS server returned a usable answer."
        }

    except dns.exception.DNSException as error:
        return {
            "domain": domain,
            "record_type": record_type,
            "records": [],
            "ttl": None,
            "latency_ms": round(
                (time.perf_counter() - start) * 1000, 2
            ),
            "status": "dns_error",
            "cache_status": "MISS",
            "message": str(error)
        }
