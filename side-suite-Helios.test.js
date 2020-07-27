jest.setMock('selenium-webdriver', webdriver);
// This file was generated using Selenium IDE
const tests = require("./commons.js");
global.Key = require('selenium-webdriver').Key;
global.URL = require('url').URL;
global.BASE_URL = configuration.baseUrl || '';
let vars = {};
jest.setTimeout(300000);
describe("", () => {
  it("", async () => {
    await tests[""](driver, vars);
    expect(true).toBeTruthy();
  });
});
beforeEach(() => {
  vars = {};
});
afterEach(async () => (cleanup()));