$( document ).ready(function() {
    var button_8 = $('button:contains("8")');
    var button_4 = $('button:contains("4")');

    var button_add = $('button:contains("+")');
    var button_sub = $('button:contains("-")');
    var button_mul = $('button:contains("*")');
    var button_div = $('button:contains("/")');

    var button_clear = $('button:contains("AC")');
    var button_res = $('button:contains("=")');

    QUnit.test( "Addition Test", function( assert ) {
        button_8.click();
        button_add.click();
        button_4.click();
        button_res.click();
        assert.equal( $('#print').val(), 12, "8 + 4 must be 12" );
        button_clear.click();
    });

    QUnit.test( "Substraction Test", function( assert ) {
        button_8.click();
        button_sub.click();
        button_4.click();
        button_res.click();
        assert.equal( $('#print').val(), 4, "8 - 4 must be 4" );
        button_clear.click();
    });

    QUnit.test( "Multiply Test", function( assert ) {
      button_8.click();
      button_mul.click();
      button_4.click();
      button_res.click();
      assert.equal( $('#print').val(), 32, "8 * 4 must be 32" );
      button_clear.click();
    });

    QUnit.test( "Division Test", function( assert ) {
      button_8.click();
      button_div.click();
      button_4.click();
      button_res.click();
      assert.equal( $('#print').val(), 2, "8 / 4 must be 2" );
      button_clear.click();
    });

        var button_5 = $('button:contains("5")');
    var button_3 = $('button:contains("3")');
    var button_1 = $('button:contains("1")');
    var button_0 = $('button:contains("0")');
    var button_sin = $('button:contains("sin")');
    var button_tan = $('button:contains("tan")');
    var button_log = $('button:contains("log")');

    QUnit.test( "Sin Test", function( assert ) {
      button_3.click();
      button_0.click();
      button_sin.click();
      assert.equal( $('#print').val(), -0.9880316240928618, "30 rad to sin must be -0.9880316240928618" );
      button_clear.click();
    });

    QUnit.test( "Tan Test", function( assert ) {
      button_4.click();
      button_5.click();
      button_tan.click();
      assert.equal( $('#print').val(), 1.6197751905438615, "45 rad to tan must be 1.6197751905438615" );
      button_clear.click();
    });

    QUnit.test( "Log Test", function( assert ) {
      button_1.click();
      button_0.click();
      button_0.click();
      button_0.click();
      button_log.click();
      assert.equal( $('#print').val(), 3, "log 1000 must be 3" );
      button_clear.click();
    });
});
