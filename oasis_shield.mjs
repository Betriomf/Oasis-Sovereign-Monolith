export class OasisShield {
  constructor(endpoint = "https://oasis-sovereign-gateway.onrender.com/v1/shield/entropy-score", timeoutMs = 350) {
    this.endpoint = endpoint;
    this.timeoutMs = timeoutMs;
  }

  async verify(intervalsMs, targetId = "client_session") {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), this.timeoutMs);

    try {
      const response = await fetch(this.endpoint, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "x-client-time": (Date.now() / 1000).toString()
        },
        body: JSON.stringify({ target_id: targetId, intervals_ms: intervalsMs }),
        signal: controller.signal
      });
      clearTimeout(timer);
      const data = await response.json();
      return { isHuman: !data.is_bot, audit: data };
    } catch (err) {
      clearTimeout(timer);
      // Fail-open: no interrumpe la navegación del cliente ante microcortes
      return { isHuman: true, audit: { fallback: true, reason: err.message } };
    }
  }
}
