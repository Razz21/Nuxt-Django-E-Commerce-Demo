export default function({ app, redirect, store }) {
  const { $axios } = app;
  $axios.onError(error => {
    const code = parseInt(error.response && error.response.status);
    if (code === 401) {
      store.commit("user/setDialog", "login");
    }
    if (code === 404) {
      redirect({ name: "404" });
    }
    return false;
  });
}
