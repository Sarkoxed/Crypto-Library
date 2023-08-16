def create_cert(cert_authority, private_key):
    one_day = datetime.timedelta(1, 0, 0)
    # Use our private key to generate a public key
    root_key = serialization.load_pem_private_key(
        private_key.encode("ascii"), password=None, backend=default_backend()
    )

    root_cert = x509.load_pem_x509_certificate(
        cert_authority.encode("ascii"), default_backend()
    )

    # Now we want to generate a cert from that root
    cert_key = rsa.generate_private_key(
        public_exponent=65537, key_size=2048, backend=default_backend()
    )
    new_subject = x509.Name(
        [
            x509.NameAttribute(NameOID.COUNTRY_NAME, u"US"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Texas"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, u"Austin"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"New Org Name!"),
        ]
    )
    cert = (
        x509.CertificateBuilder()
        .subject_name(new_subject)
        .issuer_name(root_cert.issuer)
        .public_key(cert_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.datetime.utcnow())
        .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=30))
        .add_extension(
            x509.SubjectAlternativeName([x509.DNSName(u"somedomain.com")]),
            critical=False,
        )
        .sign(root_key, hashes.SHA256(), default_backend())
    )

    # Dump to scratch
    with open("scratch/phone_cert.pem", "wb") as f:
        f.write(cert.public_bytes(encoding=serialization.Encoding.PEM))

    # Return PEM
    cert_pem = cert.public_bytes(encoding=serialization.Encoding.PEM)

    cert_key_pem = cert_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    )

    return cert_pem, cert_key_pem

