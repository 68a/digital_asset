from wtforms import *

class SettingsForm (Form):

  cny_rate = FloatField ("人民币汇率", [ validators.required(), validators.NumberRange (min=6, max=8, message='Out of range') ])

  price_diff_on = BooleanField ('差价报警开关')
  price_diff_value = FloatField ('差价报警下限（百分比）')

  def setValue ( self, in_cny_rate, in_price_diff_on, in_price_diff_value):

    self.cny_rate.data = in_cny_rate
    self.price_diff_on.data = in_price_diff_on
    self.price_diff_value.data = in_price_diff_value


    

    
    
