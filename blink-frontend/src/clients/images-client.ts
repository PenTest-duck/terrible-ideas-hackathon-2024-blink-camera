

export default class ImagesClient {
  private imagesEndpointURL = process.env.REACT_APP_LAMBDA_URL ?? "";

  public async listImages() {
    const request: RequestInfo = new Request(`${this.imagesEndpointURL}/images`, {
      method: 'GET',
    });

    return fetch(request)
      .then((res) => {console.log(res); return res.json(); })
      .then((res) => res["images"] as string[]);
  }
}