# MLOnlineandBatch
Generating Online Model Prediction and Batch Based Prediction from Same Python code

AI Platform Serving now lets you deploy your trained machine learning (ML) model with custom online prediction Python code, in beta. In this blog post, we show how custom online prediction code helps maintain affinity between your preprocessing logic and your model, which is crucial to avoid training-serving skew.

The hard work of building an ML model pays off only when you deploy the model and use it in production—when you integrate it into your pre-existing systems or incorporate your model into a novel application. If your model has multiple possible consumers, you might want to deploy the model as an independent, coherent microservice that is invoked via a REST API that can automatically scale to meet demand.

While training that model, it’s common to transform the input data into a format that improves model performance. But when performing predictions, the model expects the input data to already exist in that transformed form. For example, the model might expect a normalized numerical feature, for example TF-IDF encoding of terms in text, or a constructed feature based on a complex, custom transformation. However, the callers of your model will send “raw”, untransformed data, and the caller doesn’t (or shouldn’t) need to know which transformations are required. This means the model microservice will be responsible for applying the required transformation on the data before invoking the model for prediction.

The examples illustrate the concept clearly.
