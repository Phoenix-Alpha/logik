import json

import pulumi_aws as aws

from .common import project

integrator_center_app = aws.amplify.App(
    resource_name="integrator-center-app",
    custom_rules=[
        aws.amplify.AppCustomRuleArgs(
            source="/<*>",
            status="404-200",
            target="/index.html",
        )
    ],
    environment_variables={
        "AMPLIFY_DIFF_DEPLOY": "false",
        "AMPLIFY_MONOREPO_APP_ROOT": "src/integrator-center/frontend",
        "_LIVE_UPDATES": json.dumps(
            [{"pkg": "next-version", "type": "internal", "version": "latest"}]
        ),
    },
    iam_service_role_arn="arn:aws:iam::847186409068:role/amplifyconsole-backend-role",
    name=f"{project}-integrator-center",
    platform="WEB",
    enable_branch_auto_deletion=True,
    repository="https://github.com/nuage-studio/logik",
)

branch_develop = aws.amplify.Branch(
    resource_name="branch-develop",
    app_id=integrator_center_app.id,
    branch_name="develop",
    enable_auto_build=True,
    framework="Next.js - SSR",
    stage="PRODUCTION",
)
