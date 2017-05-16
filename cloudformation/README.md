# About Cloudformation for this Project

Since apex doesn't have many IAM features and we don't want to give the equivalent
of *:* to these functions the roles will be created by Cloudformation.

For granularity and greater control one role per function in the pipeline has been
scoped here in the CF template.

Role ARNs for Development:

  - arn:aws:iam::656532927350:role/CISLambdaFunctionRoles-StreamValidator-12UNGHKGTAIIK
  - arn:aws:iam::656532927350:role/CISLambdaFunctionRoles-StreamToIDV-T5IH2261NJZM
  - arn:aws:iam::656532927350:role/CISLambdaFunctionRoles-IDVtoIDV-8AMFBTKC70WN
  - arn:aws:iam::656532927350:role/CISLambdaFunctionRoles-IDVtoIDMDriver-22W44UZPPRSX
