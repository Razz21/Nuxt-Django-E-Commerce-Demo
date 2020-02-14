export const set = key => (state, val) => {
  state[key] = val;
};
export const get = key => state => {
  return state[key];
};
export const timeout = (duration = 1000) => {
  // async timeout
  return new Promise(resolve => {
    setTimeout(() => {
      resolve();
    }, duration);
  });
};
export const strip = (str, chars) => {
  // remove selected characters from start/end string
  // similar to Python String.strip() method
  return str
    .split(chars)
    .filter(Boolean)
    .join(chars);
};
export const parseQueryList = val => {
  return val
    ? strip(val, ",")
        .split(",")
        .map(Number)
    : false;
};

export function textRegex(val, reg) {
  const regex = new RegExp(reg).test(val);
  return regex;
}

/* =============== VUEX =============== */
export const REQUEST = ["setLoading", 1];
export const SUCCESS = ["setLoading", 2];
export const ERROR = ["setLoading", 3];

export const LOADING_HANDLERS = { REQUEST, SUCCESS, ERROR };

export const getPaginatedResults = data => data.results;
export const returnRequest = fn => () => fn;

export function queryAction(
  command,
  fn,
  RESULT,
  { REQUEST, SUCCESS, ERROR } = {}
) {
  return { run };

  async function run({ commit }) {
    REQUEST && commit(...REQUEST);
    try {
      let result = await command();
      result =
        ((typeof fn === "function" || fn instanceof Function) && fn(result)) ||
        result;
      console.log(RESULT);
      RESULT && commit(RESULT, result);
      SUCCESS && commit(...SUCCESS);
      return result;
    } catch (error) {
      console.log(RESULT, error, command);
      ERROR && commit(...ERROR, error);
      throw err;
    }
  }
}
