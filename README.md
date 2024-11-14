{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": [
                    "arn:aws:iam::람다 함수 역할 기입",
                    "arn:aws:iam::람다 함수 역할 기입2"
                ]
            },
            "Action": [
                "s3:GetObject",
                "s3:PutObject"
            ],
            "Resource": "arn:aws:s3:::버킷 이름/*"
        },
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": [
                    "arn:aws:iam::람다 함수 역할 기입",
                    "arn:aws:iam::람다 함수 역할 기입2"
                ]
            },
            "Action": "s3:ListBucket",
            "Resource": "arn:aws:s3:::버킷 이름"
        }
    ]
}
